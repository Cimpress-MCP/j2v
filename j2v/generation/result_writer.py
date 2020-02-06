from j2v.str_templates import looker_templates as lt


class LookerWriter:
    def __init__(self, output_explore_file_name, output_view_file_name,
                 sql_table_name, table_alias):
        self.output_explore_file_name = output_explore_file_name.lower() + ".explore.lkml"
        self.output_view_file_name = output_view_file_name.lower() + ".view.lkml"
        self.sql_table_name = sql_table_name
        self.table_alias = table_alias

    def create_view_file(self, views_dimensions_expr):
        """

        :return:
        """
        views_out_file = open(self.output_view_file_name, "w")
        views_out_file.write(self.get_view_str(views_dimensions_expr))
        views_out_file.close()

    def get_view_str(self, views_dimensions_expr):
        """

        :return:
        """
        views_out = list()
        for view, dimensions in views_dimensions_expr.items():
            source_table = ""
            if view == self.table_alias:
                source_table = """\n  sql_table_name: {sql_table} ;;""".format(sql_table=self.sql_table_name)
            nice_label = " ".join(view.split("_")).title()
            views_out.append(lt.view_start_str_template.format(name=view, label=nice_label, base_table=source_table))
            views_out.extend(sorted(list(dimensions)))
            views_out.append(lt.view_end_str)
        return "".join(views_out)

    def create_explore_file(self, explore_joins):
        """

        :return:
        """
        explore_out_file = open(self.output_explore_file_name, "w")
        explore_out_file.write(self.get_explore_str(explore_joins))
        explore_out_file.close()

    def get_explore_str(self, explore_joins):
        """

        :return:
        """
        explore_out = list()
        alias = self.table_alias.lower()
        nice_description = " ".join(alias.split("_")).capitalize()
        explore_out.append(
            lt.explore_start_str_template.format(explore_name=alias,
                                                 base_view_alias=alias,
                                                 base_view=alias,
                                                 description=nice_description,
                                                 label=nice_description,
                                                 view_file_name=self.output_view_file_name))
        explore_out.extend(explore_joins.values())

        explore_out.append(lt.explore_end)
        return "".join(explore_out)


class SQLWriter:
    def __init__(self, sql_table_name, table_alias):
        self.sql_table_name = sql_table_name
        self.table_alias = table_alias

    def print_sql(self, all_fields, all_joins, handle_nulls):
        if handle_nulls:
            print("\n\n ---VIEW WITH NUll VALUE HANDLING---\n\n")
        return print(self.get_sql_str(all_fields, all_joins))

    def get_sql_str(self, all_fields, all_joins):
        sql_out = list()

        sql_out.append("SELECT")
        afterSelect = True
        for view, fields in all_fields.items():
            if not afterSelect:
                sql_out[-1] += ","
            sql_out.append("---{view} Information".format(view=view))
            sql_out.append(",\n".join(sorted(list(fields.values()))))
            afterSelect = False

        source_table_sql = "FROM {table} AS {table_alias}".format(table=self.sql_table_name,
                                                                  table_alias=self.table_alias)
        if all_joins:
            source_table_sql += ","
        sql_out.append(source_table_sql)
        sql_out.append(",\n".join(all_joins))
        return "\n".join(sql_out)
