streamlit.runtime.media_file_storage.MediaFileStorageError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/la-voz-que-une/app.py", line 190, in <module>
    st.image(str(img_val), use_container_width=True)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/metrics_util.py", line 725, in wrapped_func
    result = non_optional_func(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/image.py", line 186, in image
    marshall_images(
    ~~~~~~~~~~~~~~~^
        self.dg._get_delta_path_str(),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<6 lines>...
        output_format,
        ^^^^^^^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/lib/image_utils.py", line 457, in marshall_images
    proto_img.url = image_to_url(
                    ~~~~~~~~~~~~^
        single_image, layout_config, clamp, channels, output_format, image_id
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/elements/lib/image_utils.py", line 319, in image_to_url
    url = runtime.get_instance().media_file_mgr.add(image, mimetype, image_id)
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/media_file_manager.py", line 277, in add
    file_id = self._storage.load_and_get_id(
        path_or_data, mimetype, kind, file_name
    )
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/memory_media_file_storage.py", line 155, in load_and_get_id
    self._read_file(path_or_data)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.14/site-packages/streamlit/runtime/memory_media_file_storage.py", line 208, in _read_file
    raise MediaFileStorageError(f"Error opening '{filename}'") from ex
