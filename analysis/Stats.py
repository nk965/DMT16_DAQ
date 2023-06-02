# Importing relvant libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sts
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, scale
from sklearn.linear_model import LinearRegression

def Statistics(x,y,x_err=0,y_err=1):
    # Forming the k-th Order Polynomial Regression Model for the Data
    k = 5 # Maximum order of Polynomial Regression Model
    poly_reg_aic = np.zeros(k) # Initilising the array of Akaike's Information Criterion
    for order in range(1,k+1): # Iterating through the Orders for each Polynomial Model
        poly_model = Regression_Model(x,y,order) # Calling the function RegressionModel and storing the predicted values, model, and features
        y_predicted_poly = poly_model[0] # Forming the predicted y-values for Quadratic Regression Model of the solution from the x and y data. Order = i
        poly_coef = np.zeros(order+1) # Initilising the array of all the coefficients for each regression model
        poly_coef[0], poly_coef[1:] = poly_model[1].intercept_, poly_model[1].coef_ # Extracting the y-intercept and each prefix of each order values of x.
        print('\nPolynomial Order', order, 'Coeffiecients:')
        for j in range(0,len(poly_coef)): # Iterating through the length of the poly_coef array and printing each value.
            print(poly_coef[j])      
        q = poly_model[2].shape[1] - 1 # Defining the number of parameters estimated in the model
        poly_reg_aic[order-1] = len(y)*np.log(np.sum((y - y_predicted_poly)**2)/len(y)) + 2*q # Calculate the AIC of the model for each order polynomial in the array
        plt.plot(x, y_predicted_poly, label='Poly Order:' + str(order)) # Plotting the regression model for each order polynomial
    
    # Plotting the Polynomial Models with the raw data
    plt.scatter(x, y, color='steelblue', s=2, label='Data Points') # Creating a scatter plot of the data
    plt.errorbar(x, y, yerr=y_err, xerr=x_err, ls='none', capsize=2, capthick=0.15, color='black', linewidth = 0.15)
    plt.xlabel('Time Index, X') # Labeling the x-axis: Time Index 
    plt.ylabel('Wavelength, Y') # Labeling the y-axis: Wavelength 
    plt.ylim(bottom=0)
    plt.title('Scatter Plot of Data Points with up to ' + str(k) + '-th Order \nPolynomial Regression Models') # Labelling the Title of the Model and Scatter Plot
    plt.legend(fontsize = 8, loc='upper center', frameon=False) # Forming the Legend
    plt.tight_layout() # Defining the Layout
    plt.show() # Plotting
    
    # Determining the minimum value of the Akaike's Information Criterion and the order of polynomial regression model this takes place at
    print('\nAIC:', poly_reg_aic) # Printing the array of Akaike's Information Criterion
    min_poly_reg_aic_value = np.min(poly_reg_aic) # Determines the minimum value of the AIC
    min_poly_reg_aic_order = [i+1 for i,val in enumerate(poly_reg_aic) if val==min_poly_reg_aic_value] # Determines the index/indices that this minimum occurs. Works if there are multiple locations of this minimum
    print('\nOrders of Polynomial with Smallest AIC:', min_poly_reg_aic_order, ', With Value of:', min_poly_reg_aic_value, 'nm') # Prints this minimum value and index

    # Forming the Best Polynonial Regression Models for the Data given the minimum Akaike's Information Criterion. NOTE: Here it is only at k=10
    poly_model_min = Regression_Model(x,y,min_poly_reg_aic_order[0])
    y_predicted_poly_min = poly_model_min[0] # Predicting the y-values (Wavelength) based on the calculated coefficients and the features variable
    plt.plot(x, y_predicted_poly_min, color = 'red', label='Polynomial Model Order: ' + str(min_poly_reg_aic_order[0])) # Plotting the regression model for each order polynomial of the minimum AIC
    residuals = y - y_predicted_poly_min # Calculate the vertical line lengths aka residuals
    #for i, (xi, yi, li) in enumerate(zip(x, y, residuals)): # Iterating over all x, y, and residual values
        #plt.vlines(xi, yi, yi - li, color='black', linewidth = 0.25) # Plotting Each Residual from the data point to the Fitted Polynomial Regression Line

    # Plotting the Polynomial Models with minimum AIC with the raw data
    plt.scatter(x, y, s=2, color='steelblue', label='Data Points') # Creating a scatter plot of the data
    plt.errorbar(x, y, yerr=y_err, xerr=x_err, ls='none', capsize=2, capthick=0.15, color='black', linewidth = 0.15)
    plt.xlabel('Time Index, X') # Labeling the x-axis: Time Index 
    plt.ylabel('Wavelength, Y') # Labeling the y-axis: Wavelength 
    plt.title('Scatter Plot of Data Points and the k-th Order Polynomial \nRegression Models with minimum AIC') # Labelling the Title of the Model and Scatter Plot
    plt.legend(fontsize = 8, loc='upper center', frameon=False) # Forming the Legend
    plt.tight_layout() # Defining the Layout
    plt.show() # Plotting

    # Plotting the Standardised Residuals for Polynomial Models with minimum AIC as a Q-Q plot against the Normal Distribution Line.
    residuals_stnd = scale(residuals) # Standardising the Residual Values
    pp_plot = sm.ProbPlot(residuals_stnd, fit=True) # Forming the Proability Plot that initialises the Q-Q Plot.
    qq_plot = pp_plot.qqplot(marker='.',label='Standardised Residuals of Polynomial Model Order:' + str(min_poly_reg_aic_order[0])) # Initialising the Q-Q Plot and editing some Graph Parameters.
    sm.qqline(qq_plot.axes[0], line='45') # Forming Q-Q plot with 45-degree line added to plot
    plt.xlabel('Theoretical Quantiles') # Labeling the x-axis: Theoretical Quantiles 
    plt.ylabel('Sample Quantiles') # Labeling the y-axis: Sample Quantiles 
    plt.title('Scatter Plot of Standardised Residual Values of the \nk-th Order Polynomial Regression Models with minimum AIC \nagainst Normal Distribution Line') # Labelling the Title
    plt.legend(fontsize = 8, loc='upper center', frameon=False) # Forming the Legend
    plt.tight_layout() # Defining the Layout
    plt.show() # Plotting
    
    extract_model_CI = sts.norm.ppf((1+0.95)/2)* sts.tstd(y_predicted_poly_min) / (np.sqrt(len(y_predicted_poly_min))) # Determing the 95% Confidence interval of the model itself 

    """
    # Bootstrapping the Residual Values from the extracted data. NOTE: Here it is only one at k=10
    n_bootstraps = [5,20,100] # Defining a lsit of different number of times to do the bootsrapping
    for i in range(0,len(n_bootstraps)): # Iterating through each occurrence in the list
        y_extract_predicted_poly_min_boot_iter = [] # Initialising the list of new residual values
        for n in range(n_bootstraps[i]): # Iterating through the value within the n_boostraps list to perform the bootstrapping n_bootstraps[i] times.
            resampled_residuals = bootstrap_residuals(residuals) # Resampling the residuals through random bootstrapping
            y_extract_boot = y_predicted_poly_min + resampled_residuals # Determing new values for the data given the new residual values
            model_boot = LinearRegression().fit(poly_model_min[2], y_extract_boot) # Determining a new model for the values for the wavelength
            y_extract_predicted_poly_min_boot = model_boot.predict(poly_model_min[2]) # Predicting the y-values given the Polynomial Regression Model generated for the extract data model
            y_extract_predicted_poly_min_boot_iter.append(y_extract_predicted_poly_min_boot) # Appending and storing these values for each bootstrapping iteration

        # Plotting the model with Confidence Intveral and the bootstrapped residual data confidence intervales
        boot_quantiles = np.percentile(y_extract_predicted_poly_min_boot_iter, [2.5, 97.5], axis=0) # Calculate the 0.025 and 0.975 quantiles of the predicted frequencies
        plt.fill_between(x, boot_quantiles[0], boot_quantiles[1], alpha = 0.25, color='darkorange', label = 'Bootstrapped Residual 95% Confidence Intervals') # Creating a plot of the bootstrapped data
    """
                   
    plt.fill_between(x, y_predicted_poly_min - extract_model_CI, y_predicted_poly_min + extract_model_CI, color='lightskyblue',alpha=0.5, label = 'Model 95% Confidence Intervals') # Creating a Confidence interval plot for the model
    plt.errorbar(x, y, yerr=y_err, xerr=x_err, ls='none', capsize=2, capthick=0.15, color='black', linewidth = 0.15)
    plt.plot(x, y_predicted_poly_min - extract_model_CI, color='lightskyblue') # Creating a Confidence interval plot for the lower limit of the model
    plt.plot(x, y_predicted_poly_min + extract_model_CI, color='lightskyblue') # Creating a Confidence interval plot for the upper limit of the model 
    plt.scatter(x, y, s=2, color='steelblue', label='Data Points') # Creating a scatter plot of the data
    plt.xlabel('Time Index, X') # Labeling the x-axis: Time Index 
    plt.ylabel('Wavelength, Y') # Labeling the y-axis: Wavelength 
    #plt.title('Plot of Confidence Intervals with\n' + str(n_bootstraps[i]) + ' Bootstrapping Iterations') # Labelling the Title of the Model and Scatter Plot
    plt.plot(x, y_predicted_poly_min, color='red', label='Polynomial Model Order: ' + str(min_poly_reg_aic_order[0])) # Plotting the regression model for each order polynomial of the minimum AIC
    plt.legend(fontsize = 8, loc='upper center', frameon=False) # Forming the Legend
    plt.tight_layout(pad=2.0) # Defining Layout and Padding the plots
    plt.show() # Plotting
        
    residual_std = np.std(residuals)

    # Calculate the lower and upper bounds of the error bars
    lower_bound = y_predicted_poly_min - extract_model_CI - residual_std
    upper_bound = y_predicted_poly_min + extract_model_CI + residual_std

    # Calculate the portion of intersecting data points of error bars to model CI
    intersects = ((y >= lower_bound) & (y <= upper_bound)).flatten()
    portion_intersecting = np.sum(intersects) / len(y) * 100
    
    print(f"Portion of Intersecting Data Points with Confidence Interval: {portion_intersecting:.2f}%")
    return

# Function that inputs the data and order of Polynomial Regression. Returns the predicted model for said data.
def Regression_Model(x,y,k):
    poly = PolynomialFeatures(degree=k, include_bias=False) # Forming polynomial function with degree(order) input. Also, setting bias to False since that would restict y-intercept to 0.
    poly_features = StandardScaler().fit_transform(x.reshape(-1, 1)) # Standardising, transforming and calculating the k-th order values of x in new columns.    
    poly_features = poly.fit_transform(poly_features) # Ensuring Transformation and apply Polynomial Features to the k-th order values of x in new columns. k=i here.
    poly_reg_model = LinearRegression() # Initialising the Linear Regression Model NOTE: Polynomial Regression is a linear model and therefore LinearRegression() is valid for all k.
    poly_reg_model.fit(poly_features, y) # Calculating the y-intecept and gradient coefficient of the Linear Regression Model using features variable and the result, i.e Wavelength
    y_predicted_poly = poly_reg_model.predict(poly_features) # Predicting the y-values (Wavelength) based on the calculated coefficients and the features variable
    return [y_predicted_poly, poly_reg_model, poly_features] # Function returns the Polynomial Regression Model values for the given model, the model itself and the Polynomial Features.

# Function that inputs the data and then bootstraps the data by resampling and replacing the data. Returns the resampled data
def bootstrap_residuals(data):
    resampled_data = [] # Initialising the resampled data
    for i in range(len(data)): # Iterating through the length of the input data i.e. all the data
        resample = np.random.choice(data, replace=True) # Producing and replacing a random new value given the input data
        resampled_data.append(resample) # Adding this new value to resampled_data to then be returned
    return resampled_data # Function returns the resampled data followowing the random selection and replacement of the data.

if __name__ == "__main__":

    # Reading .csv file into pandas dataframe via assignment to variable 'data'.
    # The first cell of each column in the .csv file is the column name. This is excluded from the data. 
    data = pd.read_csv('c:/Users/jimty/Documents/University/Coursework/M17_Statistics_A/Coursework/UNIT1-2023_05_26_14_38_11-CHANNEL2-temp.csv', header=0) # NOTE: Local location of .csv file

    plt.rcParams["figure.figsize"] = [18,9.5] # Forming the Size of the Plot (and all future plots)

    # Extract the data from the columns using the heading title names for the .csv read
    x = data['times_ms_buffers'].to_numpy() # x represents the time index
    y = data['temp_buffers'].to_numpy() # y represents the wavelength, measured in nanometres.
    x_err = 0
    y_err = 1

    Statistics(x,y,x_err,y_err)