run tests:
  cd Household_Budget\server
  pytest .\src\tests

or by modules:
  cd Household_Budget\server
  pytest .\src\tests\auth\test_router.py

or by specific case
  cd Household_Budget\server
  pytest .\src\tests\auth\test_router.py::test_register_user
