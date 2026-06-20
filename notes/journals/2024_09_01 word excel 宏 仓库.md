**excel  宏命令 转换公式为值** 
Sub ConvertFormulasToValues()
    Dim rng As Range
    For Each rng In Selection
        If rng.HasFormula Then
            rng.Value = rng.Value
        End If
    Next rng
End Sub


**excel  宏命令 转换工作簿所有公式为值**
Sub PasteAllSheetsAsValues()
    Dim ws As Worksheet
    On Error Resume Next ' 忽略单个工作表错误，继续处理下一个
    For Each ws In ThisWorkbook.Worksheets
        Application.CutCopyMode = False ' 清除之前的复制状态
        ws.Cells.Copy
        
        If Not IsEmpty(ws.UsedRange) Then
            ws.Cells.PasteSpecial xlPasteValues
        End If
        Application.CutCopyMode = False ' 清除剪贴板
    Next ws
    On Error GoTo 0 ' 恢复正常错误处理
End Sub

**excel拆分所有合并的单元格（OP+CO+x）**
- Sub UnmergeAllCells()
      Dim rng As Range
      Dim cell As Range
  
      '遍历所有使用的单元格
      For Each rng In ActiveSheet.UsedRange
          If rng.MergeCells Then
              rng.UnMerge
              '如果拆分后，原合并单元格中有数据，则将数据填充到拆分后的所有单元格
              For Each cell In rng
                  cell.Value = rng.Value
              Next cell
          End If
      Next rng
  End Sub

 **excel宏命令：插入模块 excel多页合并一页**
  Sub MergeSheets()
      Dim ws As Worksheet
      Dim combinedSheet As Worksheet
      
      Set combinedSheet = ThisWorkbook.Sheets.Add
      
      For Each ws In ThisWorkbook.Sheets
          If ws.Name <> combinedSheet.Name Then
              ws.UsedRange.Copy combinedSheet.Cells(combinedSheet.Cells(Rows.Count, 1).End(xlUp).Row + 1, 1)
          End If
      Next ws
  End Sub

excel宏命令：按单元格背景色求和
Function SumByColor(rng As Range, colorCell As Range) As Double
    Dim cell As Range
    Dim total As Double
    Dim colorIndex As Long
    
    colorIndex = colorCell.Interior.Color
    
    For Each cell In rng
        If cell.Interior.Color = colorIndex Then
            If IsNumeric(cell.Value) Then
                total = total + cell.Value
            End If
        End If
    Next cell
    
    SumByColor = total
End Function

excel宏命令：按单元格字体颜色求和
Function SumByFontColor(rng As Range, colorCell As Range) As Double
    Dim cell As Range
    Dim total As Double
    Dim colorIndex As Long
    
    colorIndex = colorCell.Font.Color
    
    For Each cell In rng
        If cell.Font.Color = colorIndex Then
            If IsNumeric(cell.Value) Then
                total = total + cell.Value
            End If
        End If
    Next cell
    
    SumByFontColor = total
End Function

---

**word 使用宏：对选定嵌入图片批量修改尺寸（弹窗版）** 
Sub ResizeSelectedInlinePicturesInteractive()
    Dim ilshp As InlineShape
    Dim inputHeight As String
    Dim inputWidth As String
    Dim targetHeightCm As Single
    Dim targetWidthCm As Single
    Dim foundPic As Boolean
    
    ' 弹出输入框让用户指定尺寸
    inputHeight = InputBox("请输入目标高度（厘米），仅调整高度请留宽度为空：" & vbCrLf & _
                          "（若要按宽度调整，请在此输入 0 或留空）", "调整图片尺寸", "5")
    
    If StrPtr(inputHeight) = 0 Then Exit Sub ' 用户点击取消
    
    inputWidth = InputBox("请输入目标宽度（厘米），仅调整宽度请留高度为空：" & vbCrLf & _
                         "（若要按高度调整，请在此输入 0 或留空）", "调整图片尺寸", "0")
    
    If StrPtr(inputWidth) = 0 Then Exit Sub ' 用户点击取消
    
    ' 尝试转换为数字
    On Error GoTo InvalidInput
    If inputHeight = "" Then inputHeight = "0"
    If inputWidth = "" Then inputWidth = "0"
    
    targetHeightCm = CSng(Val(inputHeight))
    targetWidthCm = CSng(Val(inputWidth))
    
    ' 至少有一个大于 0
    If targetHeightCm <= 0 And targetWidthCm <= 0 Then
        MsgBox "高度和宽度不能同时为 0 或负数。", vbExclamation
        Exit Sub
    End If
    
    ' 检查选区
    If Selection.Range.Characters.Count = 0 Then
        MsgBox "请先选中包含图片的区域。", vbExclamation
        Exit Sub
    End If
    
    foundPic = False
    For Each ilshp In Selection.InlineShapes
        If ilshp.Type = wdInlineShapePicture Then
            With ilshp
                .LockAspectRatio = msoTrue
                If targetHeightCm > 0 Then
                    .Height = CentimetersToPoints(targetHeightCm)
                ElseIf targetWidthCm > 0 Then
                    .Width = CentimetersToPoints(targetWidthCm)
                End If
            End With
            foundPic = True
        End If
    Next ilshp
    
    If foundPic Then
        MsgBox "图片尺寸已成功调整。", vbInformation
    Else
        MsgBox "选中区域内未找到嵌入型图片。", vbInformation
    End If
    
    Exit Sub
    
InvalidInput:
    MsgBox "输入无效，请输入数字。", vbCritical
End Sub

**word 使用宏：更新文中所有域** 
Sub UpdateAllFields()
    Dim doc As Document
    Set doc = ActiveDocument
    
    ' 更新正文中的域
    doc.Fields.Update
    
    ' 更新页眉和页脚中的域
    Dim sec As Section
    Dim hdrFtr As HeaderFooter
    For Each sec In doc.Sections
        For Each hdrFtr In sec.Headers
            hdrFtr.Range.Fields.Update
        Next hdrFtr
        For Each hdrFtr In sec.Footers
            hdrFtr.Range.Fields.Update
        Next hdrFtr
    Next sec
    
    ' 更新文本框、图文框等（通过故事范围 StoryRanges）
    Dim rngStory As Range
    For Each rngStory In doc.StoryRanges
        Do
            rngStory.Fields.Update
            Set rngStory = rngStory.NextStoryRange
        Loop Until rngStory Is Nothing
    Next rngStory
    
    MsgBox "所有域已更新完成！", vbInformation
End Sub