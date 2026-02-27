@echo off
echo ================================================
echo   RESTORING ALL TEST DATA
echo ================================================
echo.
echo This will create/update:
echo - 6 test user accounts (test1-test6)
echo - 4 therapist accounts
echo - Assign therapist to test1
echo.
pause

cd backend

echo.
echo ================================================
echo   Creating Test Users...
echo ================================================
python create_test_users.py

echo.
echo ================================================
echo   Creating Therapists...
echo ================================================
python create_therapists.py

echo.
echo ================================================
echo   RESTORATION COMPLETE!
echo ================================================
echo.
echo Test User Accounts:
echo -------------------
echo test1: 1000 NeuraCoins, Premium (password: 123456)
echo test2: 5000 NeuraCoins, Premium (password: 123456)
echo test3: 5000 NeuraCoins, Premium (password: 123456)
echo test4: 5000 NeuraCoins, Premium (password: 123456)
echo test5: 5000 NeuraCoins, Premium (password: 123456)
echo test6: 5000 NeuraCoins, Premium (password: 123456)
echo.
echo Therapist Accounts:
echo -------------------
echo ritvik@therapy.com (password: 123456)
echo liban@therapy.com (password: 123456)
echo yash@therapy.com (password: 123456)
echo abhisaar@therapy.com (password: 123456)
echo t1@therapy.com - t6@therapy.com (password: 123456)
echo.
echo Resources are hardcoded in the backend and will work automatically!
echo.
pause
