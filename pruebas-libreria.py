import oracledb;

print("Default array size:", oracledb.defaults.arraysize)

con = oracledb.connect(user= 'x3476452' , password= 'x3476452', dsn='oracle0.ugr.es:1521/practbd' )

print(oracledb.__version__)
print("Database version:", con.version)

con.close()