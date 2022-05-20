from app import create_app , db
from Flask_Script import Manager,Server
from  flask_Migrate import Migrate, MigrateCommand
from app.models import User,Post,Comment,Blog
#creating app instance
app = create_app('development')

manager = Manager(app)
migrate = Migrate(app,db)


manager.add_command('db',MigrateCommand)
manager.add_command('server',Server)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Post=Post,Blog=Blog, Comment=Comment)

if __name__=='__main__':
    manager.run()