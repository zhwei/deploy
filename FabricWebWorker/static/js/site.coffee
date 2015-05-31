
fullScreen = ->
  $('#log').css
    margin: '0 0 0 0',
    position: 'absolute',
    width: screen.width,
    height: screen.height


reloadLog = ->
  $.get '/log/{{ project }}/{{ function }}?ajax=true', (ret) ->
    elem = $('.pre-scrollable')
    elem.html(ret)
    elem.scrollTop(elem[0].scrollHeight)
    setTimeout(reloadLog, 1000)


action.add {
    'full-screen': fullScreen
}
