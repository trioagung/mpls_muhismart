# Script untuk update dan restart PythonAnywhere
$commands = @'
cd /home/trioagung64/mpls.muhismart
git pull origin main
touch /var/www/trioagung64_pythonanywhere_com_wsgi.py
'@

# Escape untuk SSH
$escapedCommands = $commands -replace '"', '\"'

# Jalankan SSH command
ssh trioagung64@ssh.pythonanywhere.com $escapedCommands
