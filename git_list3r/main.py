"""This tools compare websites against a git repo, then try to guess the last commit date.
Usage:
  git_list3r test [--timeout=<timeout>]
                  [--web_base=<web_base>]
                  [--file_base=<file_base>] <folder> <url>
  git_list3r version <folder>
  git_list3r -h | --help
  git_list3r --version

Options:
  -h --help               Show this help
  --version               Show the program version
  --timeout=<timeout>     The time to wait between to request in seconds [default: 0]
  --file_base=<file_base> The base file path to test files [default: .]
  --web_base=<web_base>   The base web path to test files [default: .]
"""
from docopt import docopt
import git, os, time, sys, requests, pathlib, datetime,	 urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def removeprefix(st):
	p = pathlib.Path(st)
	return pathlib.Path(*p.parts[1:])

def version(folder):
	list_file = os.path.join("__saved__", "file_list.txt")

	repo = git.Repo(folder)

	glob_max_date = 0
	glob_max_commit = "undefined"

	print("Checking versions...")
	for line in open(list_file, "r").readlines():
		if not line.strip().startswith("#"):
			time.sleep(0.5)
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

def test(folder, url, timeout, file_base, web_base):
	file_list = ["# Uncomment the lines selected for version checking"]
	save_dir = "__saved__"

	file_base = os.path.normpath(file_base)
	web_base = os.path.normpath(web_base)

	print("Testing...")
	for root, subdirs, files in os.walk(os.path.join(folder, file_base)):
		current_path = str(removeprefix(os.path.normpath(root)))

		if current_path.startswith(file_base): # Check if we are in the subfolder
			chrooted_path = current_path[len(file_base):]

			for name in files:
				uri_part = os.path.normpath(os.path.join(web_base, chrooted_path, name))
				uri = "{}/{}".format(url, uri_part)
				pth = os.path.join(current_path, name)

				time.sleep(timeout)
				sys.stdout.write("\033[K")
				sys.stdout.write(">> Testing {}\r".format(uri))
				sys.stdout.flush()
				r = requests.get(uri, verify=False)

				if r.status_code == 200:
					full = os.path.join(save_dir, str(pth))
					print("Found: {}".format(full))
					os.makedirs(os.path.dirname(full), exist_ok=True)
					open(full, "wb+").write(r.text.encode('utf-8'))
					file_list.append("# {}".format(full))

	print("Writting result to: {}/file_list.txt".format(save_dir))
	open(os.path.join(save_dir, "file_list.txt"), "w+").write("\n".join(file_list))

def main():
	args = docopt(__doc__, version='0.1')

	if args["test"] == True:
		if args["--timeout"]: float(args["--timeout"])
		return test(args["<folder>"], args["<url>"], float(args["--timeout"]), args["--file_base"], args["--web_base"])

	elif args["version"] == True:
		return version(args["<folder>"])

if __name__ == '__main__': main()
