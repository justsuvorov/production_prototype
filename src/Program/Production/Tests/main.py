import unittest

def main():
    loader = unittest.TestLoader()
    start_dir = r'C:\Users\User\Documents\production_prototype\src\Program\Production\Tests'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    main()