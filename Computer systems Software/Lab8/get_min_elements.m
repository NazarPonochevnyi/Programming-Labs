function [ min_M ] = get_min_elements(a, b, c)
    %GET_MIN_ELEMENTS
    %   Return which of the matrices has the minimum last positive element.
    
    function [ last_element ] = get_last_element(matrix)
        last_element = [];
        [m1, m2] = size(matrix);
        for k = m1 : -1 : 1
            if ~isempty(last_element)
                break
            end
            for l = m2 : -1 : 1
                element = matrix(k, l);
                if element > 0
                    last_element = element;
                    fprintf('Element %d have indeces %d and %d.\n', element, k, l)
                    break
                end
            end
        end
    end
    
    last_elements = [get_last_element(a), 
                     get_last_element(b), 
                     get_last_element(c)];
    fprintf('Last positive elements:')
    fprintf(' %i', last_elements)
    fprintf('\n')
    [~, index] = min(last_elements);
    M = ['a', 'b', 'c'];
    min_M = M(index);
end
