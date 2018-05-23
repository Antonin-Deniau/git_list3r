#!/usr/bin/env python
import git, os, sys, requests, pathlib, datetime

def removeprefix(st):
	p = pathlib.Path(st)
	return pathlib.Path(*p.parts[1:])

def usage():
	print("Usage: git_list3r <command>")
	print("                test: <folder> <url>")
	print("                version: <folder>")
	return 0

def version(args):
	if len(args) != 3:
		print("Usage git_list3r version <folder>") 
		return 0

	REPO_DIR = args[2]
	LIST_FILE = os.path.join("__saved__", "file_list.txt")

	repo = git.Repo(REPO_DIR)

	glob_max_date = 0
	glob_max_commit = "undefined"

	print("Checking versions...")
	for line in open(LIST_FILE, "r").readlines():
		if not line.strip().startswith("#"):
			pth = removeprefix(line.strip())
			commits = list(repo.iter_commits(paths=pth))

			max_date = 0
			max_commit = "undefined"

			for commit in commits:
				git_content = repo.git.show('{}:{}'.format(commits[0].hexsha, pth))
				site_content = open(line.strip(), "r").read()
				if git_content == site_content:
					dt = commit.committed_date
					if dt > max_date:
						max_date = dt
						max_commit = commit.hexsha

			if max_date > glob_max_date:
				glob_max_date = max_date
				glob_max_commit = max_commit

			if max_date != 0:
				md = datetime.datetime.fromtimestamp(max_date)
				print("{} project match at: {} (max commit: {})".format(pth, md.strftime("%d/%m/%y"), max_commit))

	gmd = datetime.datetime.fromtimestamp(glob_max_date)
	print("\nGlobal project match at: {}".format(gmd.strftime("%d/%m/%y")))
	print("Last commit: {}".format(glob_max_commit))

	return 0


def test(args):
	if len(args) != 4:
		print("Usage git_list3r test <folder> <gitrepo>") 
		return 0

	file_list = ["# Uncomment the lines selected for version checking"]

	URL = args[3]
	DIR = args[2]
	SAVE_DIR = "__saved__"

	print("Testing...")
	for root, subdirs, files in os.walk(DIR):
		for name in files:
			pth = removeprefix(os.path.join(root, name))

			r = requests.get("{}/{}".format(URL, pth))

			if r.status_code == 200:
				full = os.path.join(SAVE_DIR, str(pth))
				print("Found: {}".format(full))
				os.makedirs(os.path.dirname(full), exist_ok=True)
				open(full, "wb+").write(r.text.encode('utf-8'))
				file_list.append("# {}".format(full))

	print("Writting result to: {}/file_list.txt".format(SAVE_DIR))
	open(os.path.join(SAVE_DIR, "file_list.txt"), "w+").write("\n".join(file_list))
	return 0

def main(args):
	if len(args) < 2: return usage()
	if args[1] not in ["test", "version"]: return usage()
	if (args[1] == "test"): return test(args)
	if (args[1] == "version"): return version(args)

if __name__ == '__main__':
	exit(main(sys.argv))