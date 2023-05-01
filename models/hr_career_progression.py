from odoo import api, models
from babel.numbers import format_decimal


class HrCareerProgression(models.AbstractModel):
    _name = 'report.nerdc_hr.report_career_progression'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Career Progression"

    def generate_xlsx_report(self, workbook, data, lines):
        cr = self.env.cr
        for line in lines:
            employee_id = line.id
            employee_name = line.name
            #print(employee_id)

        sheet = workbook.add_worksheet('Career Progression')
        header_format = workbook.add_format({'bold': True, 'text_wrap': True})
        # Sky blue header
        #header_format.set_bg_color('#90EE90')
        header_format.set_font_size(10)
        cell_format = workbook.add_format()
        cell_format.set_text_wrap()
        cell_format.set_font_size(10)
        sheet.write(0, 0, 'Employment ID', header_format)
        sheet.write(0, 1, 'Firstname', header_format)
        sheet.write(0, 2, 'Lastname', header_format)
        sheet.write(0, 3, 'Organization', header_format)
        sheet.write(0, 4, 'Description', header_format)
        sheet.write(0, 5, 'Type', header_format)
        sheet.write(0, 6, 'Date Start', header_format)       
        sheet.write(0, 7, 'Date End', header_format)
        '''
        sheet.write(0, 4, 'Gender', header_format)
        sheet.write(0, 5, 'Marital Status', header_format)
        sheet.write(0, 6, 'Rank', header_format)
        sheet.write(0, 7, 'Date of First Appointment', header_format)
        sheet.write(0, 8, 'Date of Confirmation of Appointment', header_format)
        sheet.write(0, 9, 'Date of Transfer of Service', header_format)
        sheet.write(0, 10, 'Current Location', header_format)
        sheet.write(0, 11, 'Department/Unit', header_format)
        sheet.write(0, 12, 'Job Position', header_format)
        sheet.write(0, 13, 'Job Title', header_format)
        sheet.write(0, 14, 'Supervisor', header_format)
        '''
# 3089214324
        line = 0
        lines = self.env['hr.resume.line'].search([('employee_id', '=', employee_id)])
        if lines:
            for e in lines:
                line += 1
                sheet.write(line, 0,'' if not e.employee_id.employment_id else e.employee_id.employment_id, cell_format)
                sheet.write(line, 1,'' if not e.employee_id.firstname else e.employee_id.firstname.upper(), cell_format)
                sheet.write(line, 2,'' if not e.employee_id.lastname else e.employee_id.lastname.upper(), cell_format)
                sheet.write(line, 3,'' if not e.name else  e.name.upper(),  cell_format)
                sheet.write(line, 4,'' if not e.description else  e.description.upper(),  cell_format)
                sheet.write(line, 5,'' if not e.line_type_id.name else  e.line_type_id.name.upper(),  cell_format)
                sheet.write(line, 6, '' if not e.date_start else e.date_start.strftime('%Y-%m-%d') ,cell_format)
                sheet.write(line, 7, '' if not e.date_end else e.date_end.strftime('%Y-%m-%d') ,cell_format)
                #sheet.write(line, 3, '' if not e.state_id else e.state_id.name.upper(), cell_format)
                '''
                
                sheet.write(line, 4, '' if not e.gender else e.gender.upper(), cell_format)
                sheet.write(line, 5,'' if not e.marital else e.marital.upper(),cell_format)
                sheet.write(line, 6, '' if not e.grade_id else e.grade_id.name.upper(),cell_format)
                sheet.write(line, 7, '' if not e.joining_date else e.joining_date.strftime('%Y-%m-%d'),cell_format)
                sheet.write(line, 8, '' if not e.confirmation_date else e.confirmation_date.strftime('%Y-%m-%d'), cell_format)
                sheet.write(line, 9,'' if not e.promotion_date else  e.promotion_date.strftime('%Y-%m-%d'), cell_format)
                sheet.write(line, 10,'' if not e.work_location_id.name else e.work_location_id.name.upper(), cell_format)
                sheet.write(line, 11,'' if not e.department_id else e.department_id.name.upper(), cell_format)
                sheet.write(line, 12,'' if not e.job_id else e.job_id.name.upper(), cell_format)
                sheet.write(line, 13,'' if not e.job_title else e.job_title.upper(), cell_format)
                sheet.write(line, 14, '' if not e.parent_id else e.parent_id.name.upper(), cell_format) 
                '''   
