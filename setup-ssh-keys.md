# Setup SSH based access for GitHub

## Authentication with git command line

If you are analyzing a git repository that is located on GitHub and you do not have setup ssh access for that git repository on the command line, you will get the following error when trying to execute the analysis:

> Could not authenticate at remote server for fetching the latest changes. If your repository is on github, please try setting up ssh keys! You can test your configuration by executing 'git fetch -v -- origin'. If you are not prompted for a password anymore, this error should disappear.

This error is appearing because the tool uses the `git` command under the hood. When the analysis is performed it tries to execute `git fetch -v -- origin`. By default this command prompts the user for a username and password, if the repository is located on GitHub. But since it gets executed automatically in the background, no username nor password is going to be provided. 

To fix this issue you have to setup an ssh key to access your repositories on GitHub and then tell the repository to use ssh based access for interacting with the repository server.

> [!Caution]
> 
> Please have a look at [the GitHub documetnation](https://docs.github.com/en/enterprise-server@3.18/authentication/connecting-to-github-with-ssh) on how to setup the SSH keys before continuing to read!

## Setting up SSH keys for a GNU/Linux based system

### 1. Generate key pair

First you need to generate a new key pair on your local machine for your GitHub account. This can be done by executing the following command as a normal user:

```shell
ssh-keygen -t ed25519 -C "jeff@example.com"
```

The above command is going to prompt you for a directory to store the key pair (public and private key). You should put that key into the `.ssh` directory of your current user. In our example that is `/home/jeff/.ssh/github-key`. Please make sure not to specify any file extension, as it is generated automatically.

The keygen command also prompts you for a password. Leave this empty by hitting return!

> [!NOTE]
> 
> If you specified `/home/jeff/.ssh/github-key` as a destination file, then the public key of the key pair get stored in `/home/jeff/.ssh/github-key.pub`. In a later step, you need to upload the entire content of the public key file in your personal GitHub account.

### 2. Add the private key to your SSH agent

Now execute the following commands on your command line:

```shell
sudo su
exec ssh-agent zsh
ssh-add /home/jeff/.ssh/github-key
exit
```

The first command lets you switch to the root user. The second command opens a z-shell for the ssh-agent. The third adds the private key we just generated to the configuration of the ssh agent. And the last command closes our custom shell again and lets you switch back to the original shell.

### 3. Tell your SSH when to use the private key

Since we just added a fresh key to the ssh-agent we still need to configure, when that key is supposed to be used for authentication.

This can be done by editing (or creating) the file `/home/jeff/.ssh/config`. (Replace jeff with your username) and adding the following lines:

```
Host github.com
  User git
  IdentityFile ~/.ssh/github-key
```

> [!NOTE]
> 
> Always use the user `git`! Do not put in your github username here. This is necessary for authenticating at GitHub.

### 4. Configure your repository to use SSH based access

Lastly, you need to configure your repository to use ssh for connecting to the GitHub servers. 

This needs to be done for **every repository** you want to check with the static code analysis tool. First you need to navigate into the root directory of the git repository and then execute the following command:

```shell
git remote set-url origin git@github.com:<username>/<repository-name>.git
```

> [!WARNING]
> 
> Please replace `<username>` with the username of your GitHub account and `<repository-name>` with the name of the repository your are currently in.

### 5. Verify that the changes have taken effect

To verify that the previous steps were successful, you can display the configuration for your git repository by navigating into its root directory and executing:

```shell
git config --list
```

The setting `remote.origin.url` should now contain the URL we configured in step 4.

Now you can execute the final command to verify, that no password prompt is shown anymore and the ssh based access works:

```shell
git fetch -v -- origin
```


