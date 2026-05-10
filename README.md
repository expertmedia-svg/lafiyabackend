# lafiyabackend

## Production avec PM2 et Nginx

Lafiya peut etre ajoute comme un service PM2 distinct sans toucher aux autres applications deja en marche.

### PM2

Depuis le serveur, dans `/home/debian/apps/lafiyabackend`:

```bash
pm2 start ecosystem.config.cjs
pm2 save
pm2 status lafiya-backend
```

Le service ecoute en local sur `127.0.0.1:4256`.

### Nginx

Copier `nginx.lafiyabackend.conf` vers `/etc/nginx/sites-available/lafiyabackend`, puis activer le site:

```bash
sudo ln -s /etc/nginx/sites-available/lafiyabackend /etc/nginx/sites-enabled/lafiyabackend
sudo nginx -t
sudo systemctl reload nginx
```

### HTTPS

Une fois le DNS `lafiyabackend.yingr-ai.com` pointe vers le serveur:

```bash
sudo certbot --nginx -d lafiyabackend.yingr-ai.com
```
