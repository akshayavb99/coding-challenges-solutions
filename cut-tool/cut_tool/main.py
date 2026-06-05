import argparse
import sys

class CutTool:
    def __init__(self, fields, delimiter, input_content):
        self.fields = self.get_fields(fields)
        self.delimiter = delimiter
        self.input_content = input_content
    
    def get_fields(self, fields):
        if fields is None:
            return None  # meaning "select all"

        result = []

        # support both "1,2,3" and "1 2 3"
        parts = fields.replace(",", " ").split()

        for part in parts:
            f = int(part) - 1  # convert to 0-based index
            result.append(f)
        
        return result

    def get_result(self):
        try:
            result = []
            for line in self.input_content:
                fields = line.rstrip("\n").split(self.delimiter)
                if self.fields is None:
                    selected = fields
                else:
                    selected = [fields[i] for i in self.fields if i < len(fields)]
                result.append(self.delimiter.join(selected))

            return result

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")
        except IOError as e:
            raise IOError(f"Cannot read content: {e}")
        

def main():
    parser = argparse.ArgumentParser(prog='Build your own cut tool',description='Challenge to mimic the functionality of the cut command in Unix with Python', add_help = True)
        
    parser.add_argument("-f", "--fields", type = str, required = False)
    parser.add_argument('-d', '--delimiter', type = str, required = False)
    parser.add_argument('file', nargs = "?", type = str, default=None)
    
    args = parser.parse_args()
        
    if args.fields is None and args.delimiter is None:
        parser.error("Please specify a delimiter or list of fields")
    
    if not args.delimiter:
        args.delimiter = "\t" # Unix cut uses tab as the default delimiter
    
    args.file = open(args.file, 'r') if args.file and args.file != "-" else sys.stdin
    

    cut_obj = CutTool(args.fields, args.delimiter, args.file)
    for i in cut_obj.get_result():
        print(i)
    


if __name__ == "__main__":
    main()
