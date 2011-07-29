{
  'targets': [
    {
      'target_name': 'base',
      'type': 'static_library',
      'sources': [
        '../build/build_config.h',
		'port.h',
		'base_api.h',
		'basictypes.h',
		'string_piece.h',
		'string_piece.cc',
		'compiler_specific.h',
		'base_switches.h',
		'base_switches.cc',
		'atomicops.h',
		'atomicops_internals_x86_msvc.h',
		'threading/platform_thread.h',
		'threading/platform_thread_win.cc',
		'win/windows_version.h',
		'win/windows_version.cc',
		'threading/thread_restrictions.h',
		'threading/thread_restrictions.cc',
		'file_path.h',
		'file_path.cc',
		'string_util.h',
		'string_util.cc',
		'string_util_win.h',
		'stringprintf.h',
		'stringprintf.cc',
		'utf_string_conversions.h',
		'utf_string_conversions.cc',
		'utf_string_conversion_utils.h',
		'utf_string_conversion_utils.cc',
		'third_party/icu/icu_utf.h',
		'third_party/icu/icu_utf.cc',
		'eintr_wrapper.h',
		'logging.h',
		'logging.cc',
		'vlog.h',
		'vlog.cc',
		'string_split.h',
		'string_split.cc',
		'command_line.h',
		'command_line.cc',
		'string_number_conversions.h',
		'string_number_conversions.cc',
		'third_party/dmg_fp/dmg_fp.h',
		#'third_party/dmg_fp/dtoa.cc', #wrapper include this
		'third_party/dmg_fp/dtoa_wrapper.cc',
		'third_party/dmg_fp/g_fmt.cc',
		'hash_tables.h',
		'synchronization/lock.h',
		'synchronization/lock.cc',
		'synchronization/lock_impl.h',
		'synchronization/lock_impl_win.cc',
		'debug/debugger.h',
		'debug/debugger.cc',
		'debug/debugger_win.cc',
		'gtest_prod_util.h',
		'pickle.h',
		'pickle.cc',
		'at_exit.h',
		'at_exit.cc',
		'sys_string_conversions.h',
		'sys_string_conversions_win.cc',
		'string16.h',
		'string16.cc',
		'lazy_instance.h',
		'lazy_instance.cc',
		'memory/singleton.h',
		'debug/stack_trace.h',
		'debug/stack_trace.cc',
		'debug/stack_trace_win.cc',
		'threading/thread_local.h',
		'threading/thread_local_win.cc',
		'atomic_ref_count.h',
		'memory/ref_counted.h',
		'memory/ref_counted.cc',
		'memory/weak_ptr.h',
		'memory/weak_ptr.cc',
		'threading/thread_checker.h',
		'threading/thread_checker_impl.h',
		'threading/thread_checker_impl.cc',
		'threading/thread_collision_warner.h',
		'threading/thread_collision_warner.cc',
		'observer_list.h',
		'memory/scoped_handle.h',
		'memory/scoped_ptr.h',
		'bind.h',
		'bind_helpers.h',
		'bind_internal.h',
		'bind_internal_win.h',
		'callback.h',
		'callback_internal.h',
		'callback_internal.cc',
		'template_util.h',
		'time.h',
		'time.cc',
		'time_win.cc',
		'third_party/nspr/prtypes.h',
		'third_party/nspr/prtime.h',
		'third_party/nspr/prtime.cc',
		'third_party/nspr/prcpucfg.h',
		'third_party/nspr/prcpucfg_win.h',
		'cpu.h',
		'cpu.cc',
		'callback_old.h',
		'message_loop.h',
		'message_loop.cc',
		'message_loop_proxy.h',
		'message_loop_proxy.cc',
		'message_loop_proxy_impl.h',
		'message_loop_proxy_impl.cc',
		'message_pump.h',
		'message_pump.cc',
		'message_pump_win.h',
		'message_pump_win.cc',
		'message_pump_default.h',
		'message_pump_default.cc',
		'task.h',
		'task.cc',
		'tracked.h',
		'tracked.cc',
		'tracked_objects.h',
		'tracked_objects.cc',
		'synchronization/waitable_event.h',
		'synchronization/waitable_event_win.cc',
		'threading/thread.h',
		'threading/thread.cc',
		'threading/thread_local_storage.h',
		'threading/thread_local_storage_win.cc',
		'win/scoped_handle.h',
		'win/wrapped_window_proc.h',
		'win/wrapped_window_proc.cc',
		'tuple.h',
		'format_macros.h',
		'metrics/histogram.h',
		'metrics/histogram.cc',
		'debug/leak_annotations.h',
		'debug/alias.h',
		'debug/alias.cc',
      ],
      'include_dirs': [
          '..',
      ],
      # These warnings are needed for the files in third_party\dmg_fp.
      'msvs_disabled_warnings': [
        4244, 4554, 4018, 4102,
      #],
	  #'msvs_disabled_warnings': [
		  4351, 4396, 4503, 4819,
          # TODO(maruel): These warnings are level 4. They will be slowly
          # removed as code is fixed.
          4100, 4121, 4125, 4127, 4130, 4131, 4189, 4201, 4238, 4244, 4245,
          4310, 4355, 4428, 4481, 4505, 4510, 4512, 4530, 4610, 4611, 4701,
          4702, 4706,
       #],
	 #'msvs_disabled_warnings': [
          4251,  # class 'std::xx' needs to have dll-interface.
     #],
	      4275, # not dll-interface
	  ],
      'dependencies': [
        'third_party/dynamic_annotations/dynamic_annotations.gyp:dynamic_annotations',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '..',
        ],
      },
      'conditions': [
		[ 'OS == "win"', {
		# 'include_dirs': [
        #    '<(DEPTH)/third_party/wtl/include',
        # ],
          'sources!': [
            'event_recorder_stubs.cc',
            'file_descriptor_shuffle.cc',
            'message_pump_libevent.cc',
            # Not using sha1_win.cc because it may have caused a
            # regression to page cycler moz.
			#'sha1_win.cc',
            'string16.cc',
            ],
          },],
      ],
    },
  ],
}