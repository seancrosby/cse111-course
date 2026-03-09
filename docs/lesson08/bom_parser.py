# Copyright © 2026, Brigham Young University–Idaho. All rights reserved.

class BOMError(ValueError):
    """BOMError is raised if the BOM string is invalid."""

def parse_bom(bom_string, parts_catalog):
    """Convert a Bill of Materials (BOM) string into a list of 
    [PartID, Quantity].
    
    Example: "Frm:1, (Rim:1, Spk:28):2" 
    Result: [["Frm", 1.0], ["Rim", 2.0], ["Spk", 56.0]]
    """
    if not isinstance(bom_string, str):
        raise TypeError("bom_string must be a string")
    
    def get_quantity(parts_dict, part_id):
        return parts_dict.get(part_id, 0.0)

    def parse_part_qty(part_str):
        if ":" in part_str:
            name, qty = part_str.split(":", 1)
            return name.strip(), float(qty.strip())
        return part_str.strip(), 1.0

    def parse_recursive(string):
        parts_dict = {}
        i = 0
        while i < len(string):
            if string[i] == "(":
                count = 1
                start = i + 1
                for j in range(start, len(string)):
                    if string[j] == "(": count += 1
                    if string[j] == ")": count -= 1
                    if count == 0:
                        inner_dict = parse_recursive(string[start:j])
                        i = j + 1
                        multiplier = 1.0
                        if i < len(string) and string[i] == ":":
                            end = i + 1
                            while end < len(string) and (string[end].isdigit() or string[end] == "."):
                                end += 1
                            multiplier = float(string[i+1:end])
                            i = end
                        
                        for p_id, p_qty in inner_dict.items():
                            parts_dict[p_id] = get_quantity(parts_dict, p_id) + (p_qty * multiplier)
                        break
            elif string[i] == "," or string[i].isspace():
                i += 1
            else:
                start = i
                while i < len(string) and string[i] not in "(,)":
                    i += 1
                part_segment = string[start:i]
                p_id, p_qty = parse_part_qty(part_segment)
                if p_id in parts_catalog:
                    parts_dict[p_id] = get_quantity(parts_dict, p_id) + p_qty
                elif p_id:
                    raise BOMError(f"Unknown Part ID: {p_id}")
        return parts_dict

    final_dict = parse_recursive(bom_string)
    # Filter out empty keys and return as list
    return [[k, v] for k, v in final_dict.items() if k]
