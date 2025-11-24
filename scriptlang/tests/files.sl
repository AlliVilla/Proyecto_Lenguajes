# Probamos operaciones de archivos

set ruta = "tests/salida.txt"

writefile ruta "Primera linea\n"
appendfile ruta "Segunda linea\n"

readfile ruta contenido
print "Contenido del archivo:"
print contenido

deletefile ruta
log "Archivo eliminado en el test de files"
