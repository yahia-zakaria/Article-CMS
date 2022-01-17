class Config(object):
  # In a production app, store this instead in KeyVault or an environment variable
  CLIENT_SECRET = "cfc682a5-26f1-48fe-b7cf-fd64dfd8cc76" 
  AUTHORITY = "https://login.microsoftonline.com/common" 
  # For multi-tenantаpp
  # AUTHORITY = "https://login.microsoftonline.com/Enter the_Tenant_Name_Here"
                    
  CLIENT_ID = "36939ee6-fd65-4d8a-9702-20ab7f7baf08"
  REDIRECT_PATH = "/getAToken" #Used to form an absolute URL,
     # which must match your app's redirect_uri set in AAD
  # You can find the proper permission names from this document
  # https://docs.microsoft.comlen-us/graph/permissions-reference
  SCOPE = ["User.Read"] 
