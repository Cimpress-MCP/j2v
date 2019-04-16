from j2v.str_templates import looker_templates as lt


class LookerWriter:
    def __init__(self, output_explore_file_name, output_view_file_name,
                 sql_table_name):
        self.output_explore_file_name = output_explore_file_name
        self.output_view_file_name = output_view_file_name
        self.sql_table_name = sql_table_name

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
            if view == self.sql_table_name:
                source_table = """\n  sql_table_name: {sql_table} ;;""".format(sql_table=self.sql_table_name)

            views_out.append(lt.view_start_str_template.format(name=view, base_table=source_table))
            views_out.extend(dimensions)
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
        explore_out.append(
            lt.explore_start_str_template.format(explore_name=self.sql_table_name, base_view_alias=self.sql_table_name,
                                                 base_view=self.sql_table_name,
                                                 description=self.sql_table_name + " explore",
                                                 label=self.sql_table_name + " explore",
                                                 view_file_name=self.output_view_file_name))
        explore_out.extend(explore_joins.values())

        explore_out.append(lt.explore_end)
        return "".join(explore_out)


class SQLWriter:
    def __init__(self, sql_table_name):
        self.sql_table_name = sql_table_name

    def print_sql(self, all_fields, all_joins):
        return print("\n".join(self.get_sql_str(all_fields, all_joins)))

    def get_sql_str(self, all_fields, all_joins):
        sql_out = list()

        sql_out.append("SELECT")

        after_select = True
        for view, fields in all_fields.items():
            sql_out.append(("," if not after_select else "") + "\n---{view} Information".format(view=view))
            sql_out.append("\n,".join(sorted(list(fields))))
            after_select = False

        sql_out.append("FROM {table},".format(table=self.sql_table_name))
        sql_out.append("\n,".join(all_joins))
        return sql_out
