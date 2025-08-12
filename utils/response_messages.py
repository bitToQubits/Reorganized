class ResponseMessages():
    success: dict = {
        "COMPANY_SAVED": "Company saved successfully",
        "PROJECT_SAVED": "Project saved successfully",
        "MEMBERSHIP_ADDED": "User successfully added to project",
        "MEMBERSHIP_REMOVED": "User successfully removed from project",
        "PROJECTS_RETRIEVED": "Projects successfully retrieved",
        "PROJECT_DETAILS_RETRIEVED": "Project details successfully retrieved",
        "STATISTICS_RETRIEVED": "Systems statistics successfully retrieved",
        "COMPANIES_LIST_RETRIEVED": "Companies list successfully retrieved",
        "COMPANIES_USERS_LIST_RETRIEVED": "Companies users list successfully retrieved"
    }

    error: dict = {
        "OFFSET":"You must provide a valid offset for this query.",
        "USER_IS_ALREADY_IN_PROJECT": "This user is already in the specified project",
        "USER_IS_NOT_IN_PROJECT": "This user is not in the specified project",
        "ID_INTEGRITY": "The IDs must be valid for the reorganized database",
        "PROJECT_NOT_FOUND": "Project not found for the system"
    }

responses = ResponseMessages()