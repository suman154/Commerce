echo "BUILD START"
mkdir -p staticfiles_build
python3 manage.py collectstatic --noinput
python3 manage.py migrate
echo "BUILD END"
