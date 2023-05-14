# GitHub As User

---

## Common Rules

- If you have multiple GitHub accounts (like for your office) ensure the right user configurations are set in your cloned repo.
- No direct code check-in to ********main******** branch, will be disabled via an organisation rule
- Any changes to code must be tracked via an **Issue**
- Use the ************************************Create New Branch************************************ option from an issue to create a new branch, the branch name must start with the issue number
- All commit messages to your private branch should start with the issue number - **for example**

```
#3 - this is a sample commit message
```

- All merge commits needs to be verified, and should go into the main branch via merge commits

### Enabling 2FA Authentication

---

1. Install an 2FA authenticator app like **********Google’s Authenticator********** on your mobile device
2. Sign in to your account on [https://github.com/](https://github.com/)
3. From the top right icon of your account, click on the dropdown and select **Settings**
4. From under **************Access************** section on the left, select ******************************************************Password and Authentication******************************************************
5. In the "Two-factor authentication” section of the page, click **Enable two-factor authentication**.
6. Follow the instructions on the screen to setup the authentication

Detailed document can be found [here](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication)

### Creating SSH Keys for GitHub

---

In your terminal, execute the command below to create an SSH key if not present already.

```bash
ssh-keygen -t ed25519 -C "<your email id>"
```

Accept all the defaults by pressing “**Return**” or “**Enter**”.

If all goes well, you should see two files getting created in the .ssh directory.

Execute the below command to confirm if the private key and public key files are present.

```bash
ls -la ~/.ssh

total 16
drwx------   4 swateek  staff  128 Mar 27 23:08 .
drwxr-x---+ 16 swateek  staff  512 Mar 27 23:08 ..
-rw-------   1 swateek  staff  411 Mar 27 23:08 id_ed25519
-rw-r--r--   1 swateek  staff  103 Mar 27 23:08 id_ed25519.pub
```

Save these two files in your Google Drive so that this can be used every time.

### Adding SSH Keys to GitHub

---

Copy the contents of your `id_ed25519.pub` file

```bash
cat ~/.ssh/id_ed25519.pub
```

Navigate to https://github.com/settings/keys, login into your account

Click on ************************New SSH Keys************************

Provide a title, and paste the contents copied above, click ********Add SSH Keys********

### Cloning a Repository from GitHub

---

1. After having set your SSH Keys, we are now ready to clone repositories from GitHub via SSH.
2. Open any repo of your interest from this list - [https://github.com/orgs/OdiaGenAI/repositories](https://github.com/orgs/OdiaGenAI/repositories)
3. Click on the green button which says ************Code************, and select ********SSH******** tab. Copy the git command.
4. Use the below command to clone a repo -

```bash
git clone <command-that-you-copied>
# Example Below:
# git clone git@github.com:OdiaGenAI/GenerativeAI_and_LLM_Odia.git
```

1. After cloning the repo, navigate into the directory

```bash
cd <code-directory-name>
# Example Below:
# cd GenerativeAI_and_LLM_Odia
```

1. Run the below commands to ensure your credentials are correctly set

```bash
git config user.name

git config user.email
```

1. To set a desired username and email, run the below commands:
Ideally, your username should be GitHub username and email should be your email that you have registered with us

```bash
cd <code-directory-name>
git config user.name "swateekj"
git config user.email "swateek08@gmail.com"
```

### Creating an Issue

---

1. Navigate to the **************Issues************** tab of any repository and click the green button which reads ******************New Issue******************
2. Give an appropriate title, valid description and other relevant information
3. **Attach an assignee** (or multiple assignees) on the right side panel
4. ******Provide a label****** that describes the issue best
5. Add a milestone if its applicable
6. Click Save 

### Working on an Issue

---

1. Navigate to the **************Issues************** tab of any repository and select the issue you want to work with.
2. On the right side panel, towards the lower part under **********************Development**********************, you’ll see an option to create a branch.
3. Branch Names should start with the issue number (and that’s the default anyway)
4. Once a branch is created, copy the branch name and run the below commands on your local

```bash
git fetch origin
git checkout <newly-created-branch>
```

1. Now go ahead, and make code changes

### Committing a piece of code

---

1. Make changes to your files, and ensure the work is saved
2. Run the following commands on your terminal to check-in code

```bash
git add -A
# where, #3 is your issue number
git commit -m "#3 - my commit message" 
git push
```

### Raising a Pull Request

---

1. Open the GitHub repository in your browser, and select the branch you intend to raise a PR for from the dropdown.
2. Once the branch is selected, a box comes up on the with the text ********************************************Compare & Pull Request********************************************
3. Mention a merge request title, this also starts with the issue number
4. Provide appropriate description 
5. Add reviewers who’ll review the PR
6. Add assignees as yourself, since you are the one who’s creating a code change
7. Click the green button **************************************Create Pull Request**************************************
8. Reviewers would be automatically notified of a pending request
