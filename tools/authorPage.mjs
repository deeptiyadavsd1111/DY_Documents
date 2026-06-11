import { Octokit } from '@octokit/action';
import fs from 'fs';

const owner = 'CBA-General';
const repo = 'dataprotection-docs';
const path = 'docs/contributions/thanks.md';

let contributors = [];
const octokit = new Octokit();

async function fetchContributors() {
    let per_page = 1000;
    let page = 1;
    const response = await octokit.rest.repos.listContributors({
        owner: owner,
        repo: repo,
        per_page: per_page,
        page: page,
    });
    await getLogin(response.data);
}

async function getLogin(response) {
    response.forEach(user => {
        contributors.push(getUserName(user.login));
    });
    await updatePage();
}

async function getUserName(username) {
    let response = await octokit.rest.users.getByUsername({
        username,
    });
    return `${response.data.name}  \n`;
}

function handleError(err) {
    if (err)
        console.log(err)
}

async function updatePage() {
    contributors = await Promise.all(contributors);
    contributors.forEach(c => fs.appendFile('./' + path, c, handleError))
    console.log("contributors added")
}

fetchContributors();
