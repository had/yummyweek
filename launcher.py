from app import create_app

webapp = create_app("default")

if __name__ == '__main__':
    webapp.run()