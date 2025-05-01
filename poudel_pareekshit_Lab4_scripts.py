import arcpy
import pandas as pd
import matplotlib.pyplot as plt
import poudel_pareekshit_Lab4_functions as l4
import importlib
## Testing


# Block 1:  set up github
#   1.  Get set up with an account on GitHub
#   2.  Associate your GitHub account with your GitHub Desktop
#   3.  Create a new repository for this class
#   4.  Clone the repository to your local computer
#   5.  Create a new branch for your work
#   6.  Create a new folder in the repository for this class


# Block 2:  Prep and point to your Arc project for this week
#   If you have not already, create a new ArcGIS Pro project for this class
#      that is parallel to the code folder you set up in the prior step. 
#   Ensure that you have copied the files noted in the Google Doc lab document
#      from the Data/Lab4_2025 folder. 
#          
#   
# Set the workspace to point to the geodatabase you are using for this lab

arcpy.env.workspace = r"R:\2025\Spring\GEOG562\Students\poudelp\Lab_4\lab4_arcproject_pp\lab4_arcproject_pp.gdb" 

############################################################################
# Block 3:  We are going to work with the notion of extending raster objects
#   I will show you a simple example of adding functionality and then 
#   have you extend a bit further in the next block.  

#    First, reimport the lab4 functions. Remember why we need to do this? 
importlib.reload(l4)

#  Look at the code in the Lab4_functions.py file for the "SmartRaster"
#   object.  Note the method "_extract_metadata".  Test it out just to see how
#  it works.  Point to the Landsat_image_corv raster, and print out the 
#   coordinate bounds of the raster

r = l4.SmartRaster("Landsat_image_corv")
print(r.metadata["bounds"])


# Question 1
#  Why do we need to use the "super()" function in the definition of the SmartRaster?

# Your answer:
# We need to use the "super()" function because we want to define a class based on existing class and super()
# function allows us to call the methods and properties of the parent class (arcpy.Raster) within the
# child class (SmartRaster). This enables us to extend the functionality of the parent class while still
# retaining its original behavior and attributes. In this case, it allows us to access the methods and properties
# of the arcpy.Raster class while adding our own custom methods and attributes to the SmartRaster class.




# Block 4:  Add a method to the SmartRaster class to calculate the NDVI
#
#    First, UNCOMMENT MY CODE FOR CALCULATE_NDVI
#     IN THE SMARTRASTER CLASS-- THE SKELETON IS THERE
#
#
#      Go back to Lab 3 to see how we calculated the NDVI.  Use that code
#       as your basis for adding a new method to the SmartRaster class. 
#       Let's call that method "calculate_ndvi".  It should take two arguments:
#        def calculate_ndvi(self,  band4_index = 4, band3_index = 3):

#       The method should return a tuple with the okay, NDVI_object

#  Again, you'll need to add code to the calculate_ndvi function

okay, ndvi = r.calculate_ndvi()

# Assuming this is okay, write it to a new raster that we can use later
import os
#  First, check to see if the file exists.  If it does, delete it.

if okay:
        out_ndvi_file = os.path.join(
            os.path.dirname(r.raster_path),
            "NDVI"
        )
        
        if arcpy.Exists(out_ndvi_file):
            arcpy.management.Delete(out_ndvi_file)
            print("✅ Deleted existing NDVI file:", out_ndvi_file)

        ndvi.save(out_ndvi_file)
        print("✅ NDVI written to:", out_ndvi_file)
    
else:
    print("❌ NDVI calculation failed:", ndvi)

# Question 4.1 
#  In the "calculate_ndvi", the method accepts 
#    two arguments to define which band indices
#    are relevant -- band 4 and 3.  But we didn't
#    set them here -- why did it work?

#  Your answer:
# calculte_ndvi method works because in its defination, it has default values
# for band4_index and band3_index. So, it treats them as optional arguments.
# If we don't provide values for them, it uses the default values of 4 and 3 respectively.
# This makes the method work even if we don't specify the band indices when calling it.



##########################################################
# Block 5:  Now, let's look at setting up an equivalent type of
#  vector object.  This is going to be different because there
#  really isn't one in Arc the same way there is for Rasters.
#  However, when we work with feature classes, we create
#  feature layers that exist temporarily during a session, which
#  is kind of like an object.   

#  Go to lab4_functions and find the class
#   for SmartVectorLayer. 

#  UNCOMMENT THE ENTIRE CLASS (use shift /)

#  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#  Following my comment prompts in that file, 
#   fill out the code to make the 
#   "zonal_stats_to_field" method work.  

#   Then uncomment the next few lines, run them to summarize
#     the NDVI image we just created into a new
#     field called mean_ndvi



importlib.reload(l4)
fc = "Corvallis_parcels" # remember you should have copied this into your workspace in Block 2.

#Load the fc as a smart vector layer
smart_vector = l4.SmartVectorLayer(fc)

# then get the zonal stats using the mean value
smart_vector.zonal_stats_to_field(out_ndvi_file, output_field = "NDVI_mean")

# then save it as a new feature class!
smart_vector.save_as("Corvallis_parcels_plusNDVI")


# Question 5.1

#  Re-load the file in your Arc session, and the NDVI
#    file as well.  
#    Does it look like the zonal stats for NDVI worked
#     reasonably?  Any observations or oddities? 
# 

#Your answer
# Yes, the zonal stats for NDVI worked reasonably. The mean NDVI values were
# calculated for each parcel in the Corvallis_parcels feature class based on the NDVI raster.
# The oddities I observed were that some parcels had very high mean NDVI values
# higher than 0.8, which indicates a high level of vegetation cover.
# Higher than values of 0.8 indicate that there could be Sensor saturation or 
# very dense irrigated crops; values this high are uncommon.
# These high values were there even if the parcels were not in areas with dense 
# vegetation.


# Block 6: 
#  Now we'll add functionality to pull this information 
#   into a Pandas data frame


# Go to the Lab4_functions.py, uncomment all of the code
#  in the "extract_to_pandas_df" chunk of smart vector, 
#  and add the small chunk of code I have asked you
#  to do.  Most of the functionality is already there


okay, df = smart_vector.extract_to_pandas_df()


# Question 6.1. 
#  In the extract_to_pandas_df, what does it mean
#   that I define the "fields=None" in the original
#   call to the method, and how do I use it in the
#   code?  

# Your answer
# It means that the fields parameter is optional and can be omitted when calling the method.
# It tests if the fields parameter is None, if true, it automatically
# assigns the fields to all the fields in the feature class. Otherwise, 
# it uses the provided fields to extract data. This allows the user to
# either specify specific fields or extract all fields from the feature class.



#################################################
# Block 7: 
#  Now we're going to take advantage of the Pandas
#   link with matplotlib to make a graph

# First, uncomment the code for the "smartPanda" 
#  class in the lab4_functions.py, and run this code
#  below.  You can just run this -- no need to 
#  fix or add anything. 

importlib.reload(l4)

x_field = "YEAR_BUILT"
y_field = "NDVI_mean" 

sp = l4.smartPanda(df)  # create the new smartPanda type

sp.scatterplot(x_field, y_field, x_min=1901, x_max = 2030)


# question 7.1
#  in the scatterplot function, I have this piece of code:
#  if x_min is not None:
#           df_to_plot = df_to_plot[df_to_plot[x_field] >= x_min]
#  You'll note that I use the same test for x_min not being "None". 
# But what about the second line -- what is df_to_plot, 
#    and what does this line achieve? 

# Your answer:
# If x_min is given, keep only rows with YEAR_BUILT ≥ x_min;
# if x_min is None, leave the data unchanged (no lower-limit filter).

# df_to_plot is a filtered version of the original DataFrame (df)
# that only includes rows where the x_field (YEAR_BUILT) is greater than or 
# equal to x_min (if provided). This allows for dynamic filtering of the data
# based on the user's input for the x-axis minimum value.



"""
###############################################################
#  Block 8

#  For our final show, we'll read the parameters we want to make
#   the plot from an external file, and then use those to create
#   the plot and write it to a PNG graphic file.  
#  The control file with the parameters is a comma-delimted 
#   format -- .csv -- that can be easily read and written 
#   from a spreadsheet program like excel (or even just a 
#      text editor)

#  First, go into the smartPanda class and examine
#     the "plot_from_file" method. 
#  Then, copy the .csv file into your local directory.
#   Source .csv:  in the R: drive Data\Lab4_2025\params_1.csv
#   destination:  put this in your student folder in the 
#     lab4\PythonCode folder. 
#    Why?  This is where your Python interpreter is considering
#      the working directory for it (not the arcpy workspace, but
#      the python working directory to read and write files, load
#      functions,etc.)
#      Thus, you can point to the file itself without  the full
#      path if you want. 

# You have the SmartPanda as "sp" from above, right?
#   Here, and you have the name of the file for the control file
#  Below, simply call the "plot_from_file" method to run the .csv fil

param_file = 'params_1.csv'  #  this assumes you've placed in the 
                            # python code directory you're working in here. 
# Your code:



#  My code

ok = sp.plot_from_file(param_file)
if ok:
    print("Done plotting")


# Now check the output graphic and make sure it worked. 

# Now, save the .csv file under a different name, 
#   change the inputs -- either add in some 
#   x or y min, max values, or change
#    the fields. 
#   note the name of the .csv in your journal, 
#    and then save the .png file along with that in the 
#    journal. 
#   Try a couple different variants of fields and ranges

# Question 8.1
#  What will happen if you give it a field that is not
#    numeric?   How might you make this work better?

# Your answer




# Question 8.2
#  In your lab document, paste in a couple of the
#    examples of the output .png files. 



# Question 8.3
#   I don't like having to type the name of the 
#   output file because I usually just want to 
#   document the x and y variables in the filename
#   Can you describe (in words, no need for code)
#   how you might achieve that?

# Your answer:



"""