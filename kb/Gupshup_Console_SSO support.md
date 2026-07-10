<!-- kb-golden:v10 -->
# Console SSO Integration

**Module**: Console Administration

## Definition

Console SSO (Single Sign-On) integration enables organizations to authenticate users through their own identity provider (IdP) using SAML 2.0. This allows users to log in to Gupshup Console using their organization's credentials without creating separate Console accounts.

## Overview

Using Console's SSO functionality, organizations can integrate their Active Directory or any other SAML-supported identity provider with the Console platform. After SSO integration, users can log in directly using their email credentials managed by their organization's identity provider.

## When to use

- Your organization manages user identities in an external identity provider (Active Directory, Azure AD, etc.)
- You want to centralize authentication and user management
- You need to implement SAML 2.0-based Single Sign-On

## Setup path

Gupshup Console → Settings → SSO Configuration

## Prerequisites

- Admin access to Gupshup Console
- Admin access to your organization's identity provider
- SAML 2.0 support in your identity provider

## Key Features

- **Login for Users**: After SSO integration, Console users can log in directly using their email ID managed by the identity provider
- **Admin and Supervisors Support**: Console SSO is available for Admin and Supervisors roles
- **Agent Login**: Agents use a different application (Agent Assist) for login

## Configuration Requirements

### Parameters to add on Console

From your IdP server, you'll need to configure:

1. **SSO URL of the IdP Server**: The authentication endpoint URL provided by your identity provider. This URL is configured on the Console SSO settings page.

2. **Signing Certificate of the IdP**: The certificate required by the service provider to validate the signature of authentication assertions digitally signed by the IdP. Download the signing certificate from your IdP. If the certificate is not in `.pem` or `.cer` format, convert it to one of these formats before uploading.

### Parameters to add on your organization's IdP Server

Configure the following parameters on your identity provider:

- **Assertion Consumer Services (ACS) URL**: The URL where your IdP will send SAML assertions
- **Entity ID**: The unique identifier for the Console application in your IdP
- **Name ID Format**: Set to Email ID only

## Technical Integration: Azure AD SAML SSO

### Console's end setup

1. Create a SAML connection on Auth0 (or equivalent) on the appropriate tenant
2. Add temporary values for secret and metadata
3. Publish the connection and obtain:
   - Callback URL (ACS URL)
   - Entity ID
4. Share the callback URL and entity ID with the integrating party (your IdP administrator)

### IdP configuration

1. Enter the callback URL and entity ID in your IdP's SAML application settings
2. Upload the SAML signing certificate to Console
3. Provide the IdP's SSO URL to Console administration
4. Test the SSO flow with a test user account

## Troubleshooting

- If users cannot log in, verify the certificate format and ensure it's in `.pem` or `.cer` format
- Confirm that the ACS URL and Entity ID match exactly between Console and your IdP
- Check that the Name ID format is set to Email ID in your IdP
