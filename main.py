from github import Github
import argparse
import json
import requests


def _get_forks() -> None:
    forks = repo.get_forks()
    print("Total numbers of forks CTFd repo has ", forks.totalCount)


def _get_pull() -> None:
    _pulls = repo.get_pulls(state='all', base='master')
    print("Total numbers of all pull requests CTFd repo has", _pulls.totalCount)
    _pulls = repo.get_pulls(state='closed', base='master')
    print("Total numbers of closed pull requests CTFd repo has", _pulls.totalCount)
    _pulls = repo.get_pulls(state='open', base='master')
    print("Total numbers of opened pull requests CTFd repo has", _pulls.totalCount)


def _get_contributors() -> None:
    contributors = repo.get_contributors()
    print("Total number of contributors CTFd repo has", contributors.totalCount)


def _get_release() -> None:
    releases = repo.get_releases()
    _releas = []
    for _release in range(3):
        _releas.append(releases.__getitem__(index=_release).title)
        # print("These are the latest 3 releases of CTFd?", releases.__getitem__(index=_release).title)
    print("These are the latest 3 releases of CTFd", _releas)


def _get_commits() -> None:
    commits = repo.get_commits()
    print("Total numbers of commits CTFd repo has", commits.totalCount)


def _get_stars() -> None:
    stars = repo.stargazers_count
    print("Total counts of stars CTFd repo has", stars)


def _get_commit_by_user() -> None:
    userc = repo.get_contributors()
    user_login = []
    for ui in range(repo.get_contributors().totalCount):
        _user = userc.__getitem__(ui)
        user_login.append(_user.login)
    _user_login = {}
    _user_list = []
    for _login in user_login:
        cui = repo.get_commits(author=_login).totalCount
        _user_list.append((cui, _login))
    print("users commits in descending order", sorted(_user_list, reverse=True))


def _get_pr_by_user() -> None:
    _number_list = []
    pulls = repo.get_pulls(state='all', base='master')
    for _pull in range(100):
        if len(pulls.get_page(_pull)) == 0:
            break
        else:
            user_pull = pulls.get_page(_pull)
            for _number in user_pull:
                _number_list.append(_number.number)
    _pr_user = []
    headers = {'Authorization': 'token ' + _token}
    user_pull = str(repo.pulls_url)
    for _pr in _number_list:
        url = user_pull.replace("{/number}", ("/" + str(_pr)))
        request_s = requests.get(url, headers=headers)
        try:
            _request = json.loads(str(request_s.text))["user"]["login"]
            _pr_user.append(_request)
        except Exception as e:
            print("Error in PR", _pr, e)
            # raise Exception("Sorry, There is an issue with PR")

    _usr_uniq = list(dict.fromkeys(_pr_user))
    _usr_list = []
    for _usr in _usr_uniq:
        _usr_list.append((_pr_user.count(_usr), _usr))
    print("users PRs in descending order", sorted(_usr_list, reverse=True))


if __name__ == "__main__":

    with open('input.json') as _file:
        _data = json.loads(_file.read())

    try:

        parser = argparse.ArgumentParser()
        parser.add_argument("Token")
        args = parser.parse_args()
        _token = args.Token
    except:
        _token = _data["token"]
    # print(_token)
    _git: Github = Github(_token)

    _repo = _data["repo"]
    # print(_repo)
    repo = _git.get_repo(_repo)
    _get_release()
    _get_forks()
    _get_stars()
    _get_contributors()
    _get_pull()
    _get_commits()
    _get_commit_by_user()
    _get_pr_by_user()
