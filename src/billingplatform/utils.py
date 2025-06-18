import re


class QueryParser:
    def __init__(self, query_string):
        self.query_string = self._normalize_query(query_string)
        self.parsed_data = {}

    def _normalize_query(self, query):
        """Standardize whitespace and convert to uppercase keywords for easier parsing."""
        query = query.strip()
        # Convert keywords to uppercase for consistent matching
        query = re.sub(r'\b(SELECT|FROM|WHERE|AND|OR|ROWNUM|GROUP BY|HAVING|ORDER BY|ASC|DESC|OFFSET|FETCH NEXT|ROWS ONLY)\b',
                       lambda m: m.group(0).upper(), query, flags=re.IGNORECASE)
        # Reduce multiple spaces to single space
        query = re.sub(r'\s+', ' ', query)
        return query

    def parse(self):
        self._parse_select_clause()
        self._parse_from_clause()
        self._parse_where_clause()
        self._parse_group_by_clause()
        self._parse_order_by_clause()
        self._parse_pagination_clause()
        return self.parsed_data

    def _parse_select_clause(self):
        """Parses the SELECT clause."""
        match = re.match(r'SELECT\s+(.*?)(?=\s+FROM|$)', self.query_string, re.IGNORECASE)
        if match:
            field_list_str = match.group(1).strip()
            # Split by comma, considering potential subqueries within parentheses
            # This is a simplified split; true subquery parsing is complex with regex.
            fields_and_subqueries = [item.strip() for item in field_list_str.split(',') if item.strip()]
            self.parsed_data['select'] = fields_and_subqueries
            # Remove the parsed part from the query string to process remaining clauses
            self.query_string = self.query_string[match.end():].strip()
        else:
            raise ValueError("Invalid query: SELECT clause not found or malformed.")

    def _parse_from_clause(self):
        """Parses the FROM clause."""
        match = re.match(r'FROM\s+(\S+)(?=\s+(WHERE|GROUP BY|ORDER BY|OFFSET|$))', self.query_string, re.IGNORECASE)
        if match:
            self.parsed_data['from'] = match.group(1).strip()
            self.query_string = self.query_string[match.end():].strip()
        else:
            raise ValueError("Invalid query: FROM clause not found or malformed.")

    def _parse_where_clause(self):
        """Parses the WHERE clause and its conditions."""
        match = re.match(r'WHERE\s+(.*?)(?=\s+(GROUP BY|ORDER BY|OFFSET|$))', self.query_string, re.IGNORECASE)
        if match:
            conditions_str = match.group(1).strip()
            # Simple split by AND/OR. A real parser would build an AST.
            conditions = re.split(r'\s+(AND|OR)\s+', conditions_str, flags=re.IGNORECASE)
            parsed_conditions = []
            for i, part in enumerate(conditions):
                if part.upper() in ("AND", "OR"):
                    parsed_conditions.append({"operator": part.upper()})
                else:
                    parsed_conditions.append({"expression": part.strip()})
            self.parsed_data['where'] = parsed_conditions
            self.query_string = self.query_string[match.end():].strip()
        else:
            self.parsed_data['where'] = None # Clause is optional

    def _parse_group_by_clause(self):
        """Parses the GROUP BY and optional HAVING clauses."""
        match = re.match(r'GROUP BY\s+(.*?)(?:\s+HAVING\s+(.*?))?(?=\s+(ORDER BY|OFFSET|$))', self.query_string, re.IGNORECASE)
        if match:
            group_fields = [f.strip() for f in match.group(1).split(',')]
            self.parsed_data['group_by'] = {'fields': group_fields}
            if match.group(2): # Check if HAVING part exists
                self.parsed_data['group_by']['having'] = match.group(2).strip()
            self.query_string = self.query_string[match.end():].strip()
        else:
            self.parsed_data['group_by'] = None

    def _parse_order_by_clause(self):
        """Parses the ORDER BY clause."""
        match = re.match(r'ORDER BY\s+(.*?)(?=\s+(OFFSET|$))', self.query_string, re.IGNORECASE)
        if match:
            order_by_str = match.group(1).strip()
            order_by_items = []
            # Split by comma, then determine ASC/DESC
            for item in order_by_str.split(','):
                parts = item.strip().split()
                field = parts[0]
                direction = 'ASC'
                if len(parts) > 1 and parts[-1].upper() in ('ASC', 'DESC'):
                    direction = parts[-1].upper()
                order_by_items.append({'field': field, 'direction': direction})
            self.parsed_data['order_by'] = order_by_items
            self.query_string = self.query_string[match.end():].strip()
        else:
            self.parsed_data['order_by'] = None

    def _parse_pagination_clause(self):
        """Parses the OFFSET and FETCH NEXT clauses."""
        match = re.match(r'OFFSET\s+(\d+)\s+ROWS\s+FETCH\s+NEXT\s+(\d+)\s+ROWS\s+ONLY', self.query_string, re.IGNORECASE)
        if match:
            self.parsed_data['pagination'] = {
                'offset': int(match.group(1)),
                'fetch_next': int(match.group(2))
            }
            self.query_string = self.query_string[match.end():].strip()
        else:
            self.parsed_data['pagination'] = None


# --- Usage Example ---
# query = "SELECT id, name FROM users WHERE age > 25 AND city = 'New York' GROUP BY city HAVING COUNT(id) > 10 ORDER BY name DESC OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY"
# parser = QueryParser(query)
# parsed_result = parser.parse()
# import json
# print(json.dumps(parsed_result, indent=2))