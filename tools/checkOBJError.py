def scan_obj_file(file_path):
    errors = []
    try:
        with open(file_path, 'r') as obj_file:
            for line_num, line in enumerate(obj_file, start=1):
                tokens = line.strip().split()
                if len(tokens) == 0:
                    continue  # Skip empty lines
                if tokens[0] not in ['v', 'f']:
                    errors.append(f"Error at line {line_num}: Unsupported line format.")
                    continue
                if tokens[0] == 'v':
                    if len(tokens) != 4:
                        errors.append(f"Error at line {line_num}: Invalid vertex format.")
                    elif tokens[0] == 'f':
                        if len(tokens) < 4:
                            errors.append(f"Error at line {line_num}: Face must have at least 3 vertices.")
    except FileNotFoundError:
        errors.append("Error: File not found.")
    except Exception as e:
        errors.append(f"Error: {e}")
        return errors

    # Example usage
    obj_file_path = "/home/mint/AI_Source/pytorch3d/YLTset/octree.obj"
    error_list = scan_obj_file(obj_file_path)
    if error_list:
        print("Errorstest.obj found in the OBJ file:")
        for error in error_list:
            print(error)
        else:
            print("No errors found in the OBJ file.")
            
