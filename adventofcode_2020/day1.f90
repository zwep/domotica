function bubblesort(a)
     n = size(a)

    !# Traverse through all array elements
    do i = 1, n
        !# Last i elements are already in place
        do j = 1, n-i-1
            !# traverse the array from 0 to n-i-1
            !# Swap if the element found is greater
            !# than the next element
            if (a(j) > a(j+1)) then
                arr(j) = arr(j+1)
                arr(j+1) = arr(j)
            end if
        end do

    end do

end function
program readfromfile
    real, dimension(200) :: cs

    open(unit=15, file='./adventofcode_2020/day1_numbers.txt', status='old', action='read')
    read(15,*) cs
    call bubble_sort(cs)
    do i=1, last
        print *, cs(i)
    end do


end program readfromfile