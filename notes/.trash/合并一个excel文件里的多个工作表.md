Sub CombineSheets()
    Dim summarySheet As Worksheet
    Dim sheet As Worksheet
    Dim i As Integer
    Dim lastRow As Long
 '创建一个新的工作表用于汇总
    Set summarySheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
    summarySheet.Name = "Summary"
 i = 1
    '遍历所有工作表
    For Each sheet In ThisWorkbook.Sheets
        If sheet.Name <> summarySheet.Name Then
            '从第二行开始复制数据，假设第一行是标题行
            sheet.UsedRange.Offset(1, 0).Copy summarySheet.Cells(lastRow + 1, 1)
            lastRow = summarySheet.Cells(summarySheet.Rows.Count, 1).End(xlUp).Row
        End If
    Next sheet
  End Sub

Sub 合并工作簿中的所有工作表()
    Dim wb As Workbook
    Dim ws As Worksheet
    Dim targetWs As Worksheet
    Dim lastRow As Long
    Set wb = ThisWorkbook '获取当前工作簿
    '添加一个新的工作表用于存放合并后的数据，并命名为"合并后数据"
    Set targetWs = wb.Worksheets.Add(After:=wb.Sheets(wb.Sheets.Count))
    targetWs.Name = "合并后数据"
    '循环遍历工作簿中的每个工作表（除了刚新建的用于合并的工作表）
    For Each ws In wb.Worksheets
        If ws.Name <> targetWs.Name Then
            lastRow = targetWs.Cells(Rows.Count, 1).End(xlUp).Row + 1 '找到目标工作表下一个可写入数据的起始行
            ws.UsedRange.Copy Destination:=targetWs.Cells(lastRow, 1) '将当前工作表的已用区域数据复制到目标工作表
            targetWs.Cells(lastRow + ws.UsedRange.Rows.Count, 1).EntireRow.Insert '在复制完数据后插入一行空行用于分隔不同工作表的数据
        End If
    Next ws
End Sub
