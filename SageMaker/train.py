############
#Reading in data
############
df = pd.read_csv(training_dir + '/train.csv',sep=',')

############
#Preprocessing data
############
X = df.drop('Petrol_Consumption', axis = 1)
y = df['Petrol_Consumption']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

###########
#Model Building
###########
regressor = RandomForestRegressor(n_estimators=estimators)
regressor.fit(X_train, y_train)

###########
#Save the Model
###########
joblib.dump(regressor, os.path.join(args.sm_model_dir, "model.joblib"))