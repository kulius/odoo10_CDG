{
    'name': "CDG",
    'version': '1.0',
    'depends': [
        'report','report_xlsx','havelock_backend_theme','cfprint','st_dynamic_list'
    ],
    'author': "先捷電腦",
    'website': "http://www.alltop.com/",
    'category': '',
    'description': """
    
    """,
    'data': [
        'views/normal_p_view.xml',
        'views/member_base_view.xml',
        'views/member_source_view.xml',
        'views/coffin_donation_view.xml',
        'views/coffin_base_view.xml',
        'views/donate_batch_view.xml',

        'views/donate_order_view.xml',
        'views/c_worker_view.xml',
        'views/donate_single_view.xml',

        'views/consultant_base_view.xml',
        'views/cashier_base_view.xml',
        'views/poor_base_view.xml',
        'views/people_type_view.xml',

        'views/member_data_view.xml',
        'views/consultant_batch_view.xml',
        'views/member_fee_view.xml',
        'views/hand_book_view.xml',
        'views/consultant_fee_only_view.xml',
        'views/consultant_source_view.xml',
        'views/member_fee_only_view.xml',
        'views/hand_checking_view.xml',


        'report/paper.xml',
        'report/donate_batch_report.xml',
        'report/donate_single_report.xml',
        'report/cashier_list_report.xml',
        'report/consultant_list_report.xml',
        'report/member_list_report.xml',
        'report/donate_order_report.xml',
        'report/coffin_month_report.xml',
        'report/coffin_season_report.xml',
        'report/report_donate_single.xml',
        'report/donate_single_report_print.xml',
        'report/empty_cashier_report.xml',
        'report/report_cashier_roll.xml',

        'wizard/chang_donate.xml',
        'wizard/print_check.xml',
        'wizard/wizard_batch.xml',
        'wizard/new_coffin.xml',
        'wizard/coffin_batch.xml',
        'wizard/donor_search.xml',
        'wizard/member_fee_inquire.xml',
        'wizard/consultant_fee_inquire.xml',
        'wizard/donate_fee_inquire.xml',
        'wizard/coffin_inquire.xml',
        'wizard/consultant_join_year.xml',
        'wizard/consultant_fee_generate.xml',
        'wizard/member_fee_generate.xml',
        'wizard/cashier_empty.xml',
        'wizard/cashier_block_view.xml',
        'wizard/cashier_member_view.xml',
        'wizard/cashier_consultant_view.xml',
        'wizard/batch_change_print_state.xml',

        'views/charity_view.xml',

        'security/group.xml',
        'security/ir.model.access.csv',

    ],
    'demo': [],
}
