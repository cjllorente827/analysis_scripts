from ndustria import AddTask

@AddTask()
def calculate_dwarv(ds, region, line):

    ray = ds.r[
               line[0][0],
               line[0][1],
               line[0][2]:line[1][2]
            ]
    
    velocity_units = "km/s"

    ray.set_field_parameter("bulk_velocity", region.field_parameters["bulk_velocity"])
    ray.set_field_parameter("center", region.field_parameters["center"])
    
    dwarv = ray.quantities.weighted_average_quantity("radial_velocity", "density").to(velocity_units)

    return dwarv