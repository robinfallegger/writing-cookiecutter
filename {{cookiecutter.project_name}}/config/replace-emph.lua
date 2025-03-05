function Emph(el)
    return pandoc.RawInline('latex', '\\textit{' .. pandoc.utils.stringify(el) .. '}')
  end
  