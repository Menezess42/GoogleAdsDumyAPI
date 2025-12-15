# I don't need to run learning tests for this.
# I just have to add the --cov flag to the command and will run
# the coverge for it:
# pytest -v --cov tests/

# *** WARNING ****
# Never runs the --cov flag without specifying the tests/ for. Otherwise it
# will run coverage in every .py file that it encounter in the project dir.
