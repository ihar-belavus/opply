# Opply task
## Deployment info
To deploy this app on Heroku you need:
1. Login in Heroku
2. Create Heroku app
3. Create runtime.txt and add `python-3.9-buster`
4. Create Procfile and put `web: gunicorn opply.wsgi --log-file -` there
5. Commit all changes and push with `git push heroku main`


## Development
### Docker container for development
1.Use example-env as a template and put all parameters into `.env` 
2.Run `docker-compose up`

All endpoints you can see by this url after project started http://0.0.0.0:8001/swagger/
