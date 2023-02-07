import requests, zipfile, io, re, xbmcvfs, xbmcgui

notify = lambda message: xbmcgui.Dialog().notification('Script', message)

response = requests.get('https://github.com/OneAngryMan/fen.theme.ah2/zipball/master/')
if response.status_code == 200:
  zip = zipfile.ZipFile(io.BytesIO(response.content))
  files = [file for file in zip.namelist() if 'skin.arctic.horizon.2' in file and not file.endswith('/')]
  if len(files) == 0:
    notify(f'ERROR: no files in src dir')
    exit()
  xbmcvfs.rmdir(xbmcvfs.translatePath('special://masterprofile/addon_data/plugin.video.fen/custom_skins/skin.arctic.horizon.2/'),True)

  for file in files:
    with zip.open(file) as file_src:
      path_dest_file = 'special://masterprofile/addon_data/plugin.video.fen/custom_skins/' + re.sub(r'OneAngryMan.*?/','',file_src.name)
      path_dest_dir = path_dest_file.rsplit(r'/',1)[0]
      check_dir = xbmcvfs.mkdirs(xbmcvfs.translatePath(path_dest_dir))
      if not check_dir:
        notify(f'ERROR: directory creation failed')
        exit()
      with xbmcvfs.File(xbmcvfs.translatePath(path_dest_file), 'w') as file_dest:
        contents = file_src.read()
        check_file = file_dest.write(contents)
        if not check_file:
          notify(f'ERROR: file creation failed')
          exit()
  notify(f'Stored {len(files)} file(s) in userdata/addon_data/plugin.video.fen/custom_skins/...')
else:
  notify(f'ERROR: bad response status code ({str(response.status_code)})')
