# Graph POC

A small Python app using the Microsoft Graph SDK. It can run through Microsoft Dev Proxy with mocked folder responses, or call live Microsoft Graph with delegated sign-in.

## Current setup: Dev Proxy mocks

`config.json` defaults to `"client_mode": "devproxy"`. From the project directory, start Dev Proxy in one terminal:

```sh
devproxy --config-file devproxyrc.json
```

In another terminal, run the app:

```sh
uv run graph-poc
```

The app traverses the configured `folder_path` recursively. The current mock structure returns `HSBC/Fun_RFP.txt`. Add a mock response for each directory the app needs to list. Dev Proxy blocks requests that don't match a mock.

## Switch to live Microsoft Graph

When your tenant access is ready, set up an Entra app registration for a public client using device-code sign-in. Add and consent to the delegated `Files.Read` permission. This is the least-privileged delegated permission for listing drive folder contents.

Set the tenant and app registration IDs in your shell:

```sh
export ENTRA_TENANT_ID="your-tenant-id"
export ENTRA_CLIENT_ID="your-application-client-id"
```

Change `client_mode` in `config.json` to `"graph"`, then run:

```sh
uv run graph-poc
```

The app will prompt you to sign in using a device code. In Graph mode it calls Graph directly, uses normal TLS certificate verification, and does not use Dev Proxy or `mocks.json`. The configured `folder_path` remains the path relative to your OneDrive root.

If the tenant requires admin consent or blocks public-client/device-code sign-in, an administrator will need to approve the app setup. Microsoft documents the SDK client setup [here](https://learn.microsoft.com/en-us/graph/sdks/create-client) and the folder-list permission [here](https://learn.microsoft.com/en-us/graph/api/driveitem-list-children?view=graph-rest-1.0).

## Configuration

- `client_mode`: `devproxy` or `graph`
- `folder_path`: path under the signed-in user's OneDrive root
- `graph_scopes`: delegated Graph scopes; currently `Files.Read`

Use `--folder-path "some/folder"` to override the configured path for one run. Use `--config path/to/config.json` to select another config file.
