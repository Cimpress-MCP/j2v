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
        views_out = []
        for view, dimensions in views_dimensions_expr.items():
            source_table = ""
            if view == self.sql_table_name:
                source_table = """\n  sql_table_name: {sql_table} ;;""".format(sql_table=self.sql_table_name)

            views_out.append(lt.view_start_str_template.format(name=view, base_table=source_table))
            for dim in dimensions:
                views_out.append(dim)
            views_out.append(lt.view_end_str)
        return "\n".join(views_out)

    def create_explore_file(self, explore_joins):
        """

        :return:
        """
        explore_out_file = open(self.output_explore_file_name, "w")
        explore_out_file.write(
            lt.explore_start_str_template.format(explore_name=self.sql_table_name, base_view_alias=self.sql_table_name,
                                                 base_view=self.sql_table_name,
                                                 description=self.sql_table_name + " explore",
                                                 label=self.sql_table_name + " explore",
                                                 view_file_name=self.output_view_file_name))
        for explore_join in explore_joins.values():
            explore_out_file.write(explore_join)

        explore_out_file.write(lt.explore_end)
        explore_out_file.close()


class SQLWriter:
    def __init__(self, sql_table_name):
        self.sql_table_name = sql_table_name

    def print_sql(self, all_fields, all_joins):
        print("SELECT")

        after_select = True
        for view, fields in all_fields.items():
            print(("," if not after_select else "") + "\n---{view} Information".format(view=view))
            print("\n,".join(sorted(list(fields))))
            after_select = False

        print("FROM {table},".format(table=self.sql_table_name))
        print("\n,".join(all_joins))
