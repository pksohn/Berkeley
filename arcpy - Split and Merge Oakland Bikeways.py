import arcpy
import os

arcpy.env.workspace = "C:\Users\pksohn\Desktop\Bikeway GIS"
arcpy.env.overwriteOutput = True

# to shorten the file paths below
mainfolder = "C:\Users\pksohn\Desktop\Bikeway GIS"
subfolder = "C:\Users\pksohn\Desktop\Bikeway GIS\Secondary Shapefiles"

''' OAKLAND ANALYSIS '''

# shapefile names
oak_bike = mainfolder+"\\Original Sources\\Oakland Bikeways\\bikeways.shp"
al_road = mainfolder+"\\Original Sources\\tl_2010_06001_roads\\tl_2010_06001_roads.shp"
al_tract = mainfolder+"\\Original Sources\\tl_2010_06001_tract10\\tl_2010_06001_tract10.shp"
CA_place = mainfolder+"\\Original Sources\\tl_2010_06_place10\\tl_2010_06_place10.shp"

# Get Oakland City boundaries from California Place file
arcpy.Select_analysis(CA_place, subfolder+"\Oakland_City.shp", """ "NAME10" = 'Oakland' """)
oak_boundaries = subfolder+"\Oakland_City.shp"

# Clip Oakland features from Alameda County files

arcpy.Clip_analysis(al_road, oak_boundaries, subfolder+"\Oakland_Roads.shp")
oak_road = subfolder+"\Oakland_Roads.shp"

arcpy.Clip_analysis(al_tract, oak_boundaries, subfolder+"\Oakland_Tracts.shp")
oak_tracts = subfolder+"\Oakland_Tracts.shp"

# Processing Oakland road file
# Split Oakland road features into tracts
arcpy.Split_analysis(oak_road, oak_tracts, "NAME10", mainfolder+"\Splits\Oakland Roads")

oak_road_splits = []

for f in os.listdir(mainfolder+"\Splits\Oakland Roads"):
     if f[-4:] == '.shp':
     	oak_road_splits.append(f)      

arcpy.env.workspace = mainfolder+"\Splits\Oakland Roads"
arcpy.Merge_management(oak_road_splits, subfolder+"\Oakland_Roads_Tract.shp",)
oak_road_tracts = subfolder+"\Oakland_Roads_Tract.shp"

# Calculate length of roads
arcpy.AddField_management(oak_road_tracts, "roadlength", "float")
arcpy.CalculateField_management(oak_road_tracts, "roadlength","!shape.length@miles!", "PYTHON")

# Spatial join road length sum to tract file

fm = arcpy.FieldMappings()
fm.addTable(oak_tracts)
fm.addTable(oak_road_tracts)
FieldIndex = fm.findFieldMapIndex("roadlength")
fieldmap = fm.getFieldMap(FieldIndex)
fieldmap.mergeRule = "sum"
fm.replaceFieldMap(FieldIndex, fieldmap)

arcpy.SpatialJoin_analysis(oak_tracts, oak_road_tracts, subfolder+"\Oakland_Tracts_v2.shp","JOIN_ONE_TO_ONE","KEEP_ALL",fm,"CONTAINS")
oak_tracts_2 = subfolder+"\Oakland_Tracts_v2.shp"

# Processing Oakland bike file
# Split Oakland bike features into tracts
arcpy.Split_analysis(oak_bike, oak_tracts, "NAME10", mainfolder+"\Splits\Oakland Bikeways")

oak_bike_splits = []

for f in os.listdir(mainfolder+"\Splits\Oakland Bikeways"):
     if f[-4:] == '.shp':
     	oak_bike_splits.append(f)      

arcpy.env.workspace = mainfolder+"\Splits\Oakland Bikeways"
arcpy.Merge_management(oak_bike_splits, subfolder+"\Oakland_Bike_Tract.shp")
oak_bike_tracts = subfolder+"\Oakland_Bike_Tract.shp"

# Calculate length of bikeways
arcpy.AddField_management(oak_bike_tracts, "bikelength", "float")
arcpy.CalculateField_management(oak_bike_tracts, "bikelength","!shape.length@miles!", "PYTHON")

# Spatial join road length sum to tract file
fm2 = arcpy.FieldMappings()
fm2.addTable(oak_tracts_2)
fm2.addTable(oak_bike_tracts)
FieldIndex2 = fm2.findFieldMapIndex("bikelength")
fieldmap2 = fm2.getFieldMap(FieldIndex2)
fieldmap2.mergeRule = "sum"
fm2.replaceFieldMap(FieldIndex2, fieldmap2)

# Remove extraneous fields from bike file
fm2.removeFieldMap(fm2.findFieldMapIndex("OID_"))
fm2.removeFieldMap(fm2.findFieldMapIndex("Name"))
fm2.removeFieldMap(fm2.findFieldMapIndex("FolderPath"))
fm2.removeFieldMap(fm2.findFieldMapIndex("SymbolID"))
fm2.removeFieldMap(fm2.findFieldMapIndex("AltitudeMO"))
fm2.removeFieldMap(fm2.findFieldMapIndex("Clamped"))
fm2.removeFieldMap(fm2.findFieldMapIndex("Extruded"))
fm2.removeFieldMap(fm2.findFieldMapIndex("Snippet"))
fm2.removeFieldMap(fm2.findFieldMapIndex("PopupInfo"))

arcpy.SpatialJoin_analysis(oak_tracts_2, oak_bike_tracts, subfolder+"\Oakland_Tracts_v3.shp","JOIN_ONE_TO_ONE","KEEP_ALL",fm2,"CONTAINS")
oak_tracts_3 = subfolder+"\Oakland_Tracts_v3.shp"

# Calculate bikeway proportion

arcpy.AddField_management(oak_tracts_3, "bikeprop", "float")
arcpy.CalculateField_management(oak_tracts_3, "bikeprop","!bikelength!/!roadlength!","PYTHON")

''' SF ANALYSIS'''

# shapefile names
SF_bike = mainfolder+"\\Original Sources\\mta_Bicycle_Route_Network\\mta_Bicycle_Route_Network.shp"
SF_road = mainfolder+"\\Original Sources\\tl_2010_06075_roads\\tl_2010_06075_roads.shp"
SF_tract = mainfolder+"\\Original Sources\\tl_2010_06075_tract10\\tl_2010_06075_tract10.shp"

# Processing SF road file
# Split SF road features into tracts
arcpy.Split_analysis(SF_road, SF_tract, "NAME10", mainfolder+"\Splits\SF Roads")

SF_road_splits = []

for f in os.listdir(mainfolder+"\Splits\SF Roads"):
     if f[-4:] == '.shp':
     	SF_road_splits.append(f)      

arcpy.env.workspace = mainfolder+"\Splits\SF Roads"
arcpy.Merge_management(SF_road_splits, subfolder+"\SF_Roads_Tract.shp",)
SF_road_tracts = subfolder+"\SF_Roads_Tract.shp"

# Calculate length of roads
arcpy.AddField_management(SF_road_tracts, "roadlength", "float")
arcpy.CalculateField_management(SF_road_tracts, "roadlength","!shape.length@miles!", "PYTHON")

# Spatial join road length sum to tract file

fm3 = arcpy.FieldMappings()
fm3.addTable(SF_tract)
fm3.addTable(SF_road_tracts)
FieldIndex3 = fm3.findFieldMapIndex("roadlength")
fieldmap3 = fm3.getFieldMap(FieldIndex3)
fieldmap3.mergeRule = "sum"
fm3.replaceFieldMap(FieldIndex3, fieldmap3)

arcpy.SpatialJoin_analysis(SF_tract, SF_road_tracts, subfolder+"\SF_Tracts_v2.shp","JOIN_ONE_TO_ONE","KEEP_ALL",fm3,"CONTAINS")
SF_tracts_v2 = subfolder+"\SF_Tracts_v2.shp"

# Processing SF bike file
# Split SF bike features into tracts
arcpy.Split_analysis(SF_bike, SF_tract, "NAME10", mainfolder+"\Splits\SF Bikeways")

SF_bike_splits = []

for f in os.listdir(mainfolder+"\Splits\SF Bikeways"):
     if f[-4:] == '.shp':
     	SF_bike_splits.append(f)      

arcpy.env.workspace = mainfolder+"\Splits\SF Bikeways"
arcpy.Merge_management(SF_bike_splits, subfolder+"\SF_Bike_Tract.shp")
SF_bike_tracts = subfolder+"\SF_Bike_Tract.shp"

# Calculate length of bikeways
arcpy.AddField_management(SF_bike_tracts, "bikelength", "float")
arcpy.CalculateField_management(SF_bike_tracts, "bikelength","!shape.length@miles!", "PYTHON")

# Spatial join road length sum to tract file
fm4 = arcpy.FieldMappings()
fm4.addTable(SF_tracts_v2)
fm4.addTable(SF_bike_tracts)
FieldIndex4 = fm4.findFieldMapIndex("bikelength")
fieldmap4 = fm4.getFieldMap(FieldIndex4)
fieldmap4.mergeRule = "sum"
fm4.replaceFieldMap(FieldIndex4, fieldmap4)

arcpy.SpatialJoin_analysis(SF_tracts_v2, SF_bike_tracts, subfolder+"\SF_Tracts_v3.shp","JOIN_ONE_TO_ONE","KEEP_ALL",fm4,"CONTAINS")
SF_tracts_3 = subfolder+"\SF_Tracts_v3.shp"

# Calculate bikeway proportion

arcpy.AddField_management(SF_tracts_3, "bikeprop", "float")
arcpy.CalculateField_management(SF_tracts_3, "bikeprop","!bikelength!/!roadlength!", "PYTHON")
