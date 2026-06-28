#r/tools/Excel

- 方法一（效果好）
- Sub ConvertFormulasToValues()
  Dim rng As Range
  Set rng = Selection '这里的 Selection 表示当前选中的区域，也可以指定特定的单元格区域，比如 Sheets("SheetI rng. Value rng. Value
  End Sub
-
- 方法二（效果还可以）
- Sub ConvertFormulasToValues()
      Dim rng As Range
      For Each rng In Selection
          If rng.HasFormula Then
              rng.Value = rng.Value
          End If
      Next rng
  End Sub