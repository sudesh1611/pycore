from typing import Dict

class BlackduckProjectConfig:
    # Blackduck Project Name and ID mapping that needs to be parsed
    
    #
    # Example
    #
    # PROJECT_NAME_ID_MAPPING = {
    #     "SunShine_Docker": "fba46117-aabb-ccdd-abcd-1234567895",
    #     "Project_Name_2": "fba46117-aabb-ccdd-abcd-123456789"
    # }

    # Update Here
    PROJECT_NAME_ID_MAPPING = {
        
    }


    # Don't Update This
    PROJECT_ID_NAME_MAPPING: Dict[str, str] = {}
    for key, value in PROJECT_NAME_ID_MAPPING.items():
        PROJECT_ID_NAME_MAPPING[value] = key