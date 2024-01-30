# Import required modules from Revit API
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, FamilyInstance, Transaction, XYZ
from Autodesk.Revit.DB import IndependentTag, TagMode, Reference

# Get the current document
doc = __revit__.ActiveUIDocument.Document

# Function to place fire alarm device tag
def place_fire_alarm_device_tag(doc, family_symbol_name, tag_family_name):
    # Start a transaction
    transaction = Transaction(doc, "Place Fire Alarm Device Tag")
    transaction.Start()

    try:
        # Find the family instance by family symbol name
        collector = FilteredElementCollector(doc)
        family_instances = collector.OfCategory(BuiltInCategory.OST_FireAlarmDevices).OfClass(FamilyInstance).ToElements()

        for instance in family_instances:
            if instance.Symbol.Name == family_symbol_name:
                # Get the insertion point of the family instance
                location = instance.Location.Point
                tag_point = XYZ(location.X, location.Y, location.Z + 10.0)  # Offset the tag above the family instance

                # Find the tag family by name
                tag_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Tags).OfClass(FamilyInstance).ToElements()
                for tag_family in tag_collector:
                    if tag_family.Name == tag_family_name:
                        # Place tag above the family instance
                        tag = IndependentTag.Create(doc, doc.ActiveView.Id, Reference(instance), True, TagMode.TM_ADDBY_CATEGORY, TagMode.TM_ADDBY_CATEGORY, tag_point, None, False)
                        tag.ChangeTypeId(tag_family.GetTypeId())  # Set the tag family type
                        break

                break

        # Commit the transaction
        transaction.Commit()
        print("Fire alarm device tag placed successfully.")

    except Exception as e:
        # Rollback the transaction in case of error
        transaction.RollBack()
        print("Error:", e)

# Call the function with the specified family symbol and tag family names
family_symbol_name = "3m"
tag_family_name = "M_Fire Alarm Device Tag"
place_fire_alarm_device_tag(doc, family_symbol_name, tag_family_name)
