
```yaml
  CognitoUserPoolClient:
    Type: AWS::Cognito::UserPoolClient
    Properties:
      ClientName: CognitoUserPoolClient
      UserPoolId: !Ref CognitoUserPool
      AllowedOAuthFlows:
      - implicit
      AllowedOAuthFlowsUserPoolClient: true
      AllowedOAuthScopes:
      - email
      - openid
      LogoutURLs:
      - !Sub 
        - https://um-app.${ Domain }
        - Domain: !ImportValue UserManagerApp-RootDomain
      CallbackURLs:
      - !Sub 
        - https://um-app.${ Domain }
        - Domain: !ImportValue UserManagerApp-RootDomain
      SupportedIdentityProviders:
      - COGNITO  
```