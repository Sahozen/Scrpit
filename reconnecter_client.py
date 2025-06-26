#!/usr/bin/env python3
# reconnecter_client.py

import subprocess
import datetime


def monter_partage(partage, point_montage):
    try:
        # Vérifie si le point de montage est déjà utilisé
        result = subprocess.run(
            ['findmnt', point_montage],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            print(f"[INFO] Le point de montage {point_montage} est déjà monté.")
            return

        # Monte le partage CIFS
        subprocess.run(
            [
                'mount', '-t', 'cifs',
                partage,
                point_montage,
                '-o',
                'credentials=/etc/samba/user.cred,iocharset=utf8,sec=ntlmssp,'
                'uid=thomas,gid=thomas,file_mode=0660,dir_mode=0770'
            ],
            check=True
        )

        print(f"[SUCCÈS] Montage réussi pour {partage} sur {point_montage}.")
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Impossible de monter {partage} : {e}")


def main():
    partages = {
        "//192.168.10.253/NAS1": "/mnt/nas1",
        "//192.168.10.253/NAS2": "/mnt/nas2"
    }

    # Au démarrage, on tente de monter chaque partage
    print("[INFO] Début de la reconnexion au démarrage...")
    for partage, point_montage in partages.items():
        monter_partage(partage, point_montage)
    print("[INFO] Processus terminé.")


if _name_ == "_main_":
    main()
