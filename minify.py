import argparse
import ffmpeg
import os
import glob

def compress(input, output):
	print(f"Compressing {input} to {output}")

	inp = ffmpeg.input(input)

	crf = "18" # 18 is considered visually lossless
	outp = ffmpeg.output(inp, output, crf=crf, vcodec="libx265", preset="slow")

	try:
		ffmpeg.run(outp, overwrite_output=False)
	except ffmpeg.Error as e:
		print(e.stderr.decode())
		return False

	try:
		ffmpeg.probe(output)
		return True
	except ffmpeg.Error as e:
		print(e.stderr.decode())
		return False

def process_dir(dir, ext="mp4"):
	print(f"Processing directory {dir}")
	files = glob.glob(f"{dir}/*.{ext}")

	for file in files:
		output = f"{os.path.splitext(file)[0]}_compressed.{ext}"
		if compress(file, output):
			origSize = os.path.getsize(file)
			newSize = os.path.getsize(output)
			if newSize < origSize:
				print(f"Removing original file {file}")
				os.remove(file)
			else:
				print(f"Removing compressed file {output}")
				os.remove(output)
		else:
			print(f"Failed to compress {file}")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Compresses vids")
	parser.add_argument("--input", type=str, help="Input file")
	parser.add_argument("--output", type=str, help="Output file")
	parser.add_argument("--dir", type=str, help="Directory to process")
	args = parser.parse_args()

	if args.dir:
		process_dir(args.dir)
	elif args.input and args.output:
		compress(args.input, args.output)
	else:
		print("No --input, --output, or --dir specified")