#!/usr/bin/python2.4
# Copyright (c) 2006-2008 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

'''Item formatters for RC headers.
'''

import re

from grit.format import interface
from grit import exception
from grit import util

from grit.extern import FP


class TopLevel(interface.ItemFormatter):
  '''Writes the necessary preamble for a resource.h file.'''

  def Format(self, item, lang='', begin_item=True, output_dir='.'):
    if not begin_item:
      return ''
    else:
      header_string = '''// Copyright (c) Google Inc. %d
// All rights reserved.
// This file is automatically generated by GRIT. Do not edit.

#pragma once
''' % (util.GetCurrentYear())
      # Check for emit nodes under the rc_header. If any emit node
      # is present, we assume it means the GRD file wants to override
      # the default header, with no includes.
      for output_node in item.GetOutputFiles():
        if output_node.GetType() == 'rc_header':
          for child in output_node.children:
            if child.name == 'emit':
              if child.attrs['emit_type'] == 'prepend':
                return header_string
      # else print out the default header with include
      return header_string + '''
#include <atlres.h>

'''


class EmitAppender(interface.ItemFormatter):
  '''Adds the content of the <emit> nodes to the RC header file.'''

  def Format(self, item, lang='', begin_item=True, output_dir='.'):
    if not begin_item:
      return ''
    else:
      return '%s\n' % (item.GetCdata())

class Item(interface.ItemFormatter):
  '''Writes the #define line(s) for a single item in a resource.h file.  If
  your node has multiple IDs that need to be defined (as is the case e.g. for
  dialog resources) it should define a function GetTextIds(self) that returns
  a list of textual IDs (strings).  Otherwise the formatter will use the
  'name' attribute of the node.'''

  # All IDs allocated so far, mapped to the textual ID they represent.
  # Used to detect and resolve collisions.
  ids_ = {}

  # All textual IDs allocated so far, mapped to the numerical ID they
  # represent. Used when literal IDs are being defined in the 'identifiers'
  # section of the GRD file to define other message IDs.
  tids_ = {}

  def _VerifyId(self, id, tid, msg_if_error):
    if id in self.ids_ and self.ids_[id] != tid:
      raise exception.IdRangeOverlap(msg_if_error +
        '\nUse the first_id attribute on grouping nodes (<structures>,\n'
        '<includes>, <messages> and <ids>) to fix this problem.')
    if id < 101:
      print ('WARNING: Numeric resource IDs should be greater than 100 to avoid\n'
             'conflicts with system-defined resource IDs.')

  def Format(self, item, lang='', begin_item=True, output_dir='.'):
    if not begin_item:
      return ''

    # Resources that use the RES protocol don't need
    # any numerical ids generated, so we skip them altogether.
    # This is accomplished by setting the flag 'generateid' to false
    # in the GRD file.
    if 'generateid' in item.attrs:
      if item.attrs['generateid'] == 'false':
        return ''

    text_ids = item.GetTextualIds()

    # We consider the "parent" of the item to be the GroupingNode containing
    # the item, as its immediate parent may be an <if> node.
    item_parent = item.parent
    import grit.node.empty
    while item_parent and not isinstance(item_parent,
                                         grit.node.empty.GroupingNode):
      item_parent = item_parent.parent

    lines = []
    for tid in text_ids:
      if util.SYSTEM_IDENTIFIERS.match(tid):
        # Don't emit a new ID for predefined IDs
        continue

      # Some identifier nodes can provide their own id,
      # and we use that id in the generated header in that case.
      if hasattr(item, 'GetId') and item.GetId():
        id = long(item.GetId())

      elif ('offset' in item.attrs and item_parent and
            'first_id' in item_parent.attrs and item_parent.attrs['first_id'] != ''):
         offset_text = item.attrs['offset']
         parent_text = item_parent.attrs['first_id']

         try:
          offset_id = long(offset_text)
         except ValueError:
          offset_id = self.tids_[offset_text]

         try:
          parent_id = long(parent_text)
         except ValueError:
          parent_id = self.tids_[parent_text]

         id = parent_id + offset_id

      # We try to allocate IDs sequentially for blocks of items that might
      # be related, for instance strings in a stringtable (as their IDs might be
      # used e.g. as IDs for some radio buttons, in which case the IDs must
      # be sequential).
      #
      # We do this by having the first item in a section store its computed ID
      # (computed from a fingerprint) in its parent object.  Subsequent children
      # of the same parent will then try to get IDs that sequentially follow
      # the currently stored ID (on the parent) and increment it.
      elif not item_parent or not hasattr(item_parent, '_last_id_'):
        # First check if the starting ID is explicitly specified by the parent.
        if (item_parent and 'first_id' in item_parent.attrs and
            item_parent.attrs['first_id'] != ''):
          id = long(item_parent.attrs['first_id'])
          self._VerifyId(id, tid,
            'Explicitly specified numeric first_id %d conflicts with one of the\n'
            'ID ranges already used.' % id)
        else:
          # Automatically generate the ID based on the first clique from the
          # first child of the first child node of our parent (i.e. when we
          # first get to this location in the code).

          # According to
          # http://msdn.microsoft.com/en-us/library/t2zechd4(VS.71).aspx
          # the safe usable range for resource IDs in Windows is from decimal
          # 101 to 0x7FFF.

          id = FP.UnsignedFingerPrint(tid)
          id = id % (0x7FFF - 101)
          id += 101

          self._VerifyId(id, tid,
            'Automatic (fingerprint-based) numeric ID for %s (%d) overlapped\n'
            'with a previously allocated range.' % (tid, id))

        if item_parent:
          item_parent._last_id_ = id
      else:
        assert hasattr(item_parent, '_last_id_')
        id = item_parent._last_id_ = item_parent._last_id_ + 1
        self._VerifyId(id, tid,
          'Wanted to make numeric value for ID %s (%d) follow the numeric value of\n'
          'the previous ID in the .grd file, but it was already used.' % (tid, id))

      if tid not in self.ids_.values():
        self.ids_[id] = tid
        self.tids_[tid] = id
        lines.append('#define %s %d\n' % (tid, id))
    return ''.join(lines)

