echo "Se descargaran 6.8 GiB de datos"
read -p "Está de acuerdo? [y/N] " -n 1 -r
echo    
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
fi

# gdown?
if ! command -v gdown &> /dev/null
then
    echo "Debe instalar gdown primero!"
    echo "run `pip install gdown`"
    exit
fi

gdown --folder -O input 1KhlclNOiD1WwB34p5t6HgzHJa93s5PMl