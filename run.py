from market import app
print(f" app wali file {app}")
#Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run(debug=True,port=8000)